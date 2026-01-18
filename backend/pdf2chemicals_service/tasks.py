import os
import json
import subprocess
import uuid
import logging
from celery import chain, group, shared_task
from celery.result import AsyncResult
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from tasks.models import UserTask
from tasks.util.tasks import BaseTask
from user.models import User
from pdf2chemicals_service.util.tasks import ChainedTask
from chemicals.tasks import post_chemical
from .util.util import file_exists, remove_file
from .cluster import (
    ResourceUnavailable,
    ClusterNodeManager,
    generate_pbs_script,
    is_pbs_job_completed
)
from .cleanup import cleanup_pdf2chemicals_resources

logger = logging.getLogger(__name__)


# ============================================================================
# MAIN ORCHESTRATION TASK
# ============================================================================

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_extract_and_save_chemicals_from_pdf',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    autoretry_for=(Exception,),
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def extract_and_save_chemicals_from_pdf(self, *args, **kwargs):
    """
    Main orchestration task for PDF processing workflow.
    
    Creates a chain: PDF script → HPC submit → Monitor → Load → Save → Return result
    
    Args:
        task_id (str, optional): Explicit task ID. Auto-generated if not provided.
        user_id (int): User requesting the processing
        pdf_path (str): Relative path to PDF in MEDIA_ROOT
        original_filename (str): Original PDF filename
        export_format (str): Output format (json, sdf, mol, etc.)
        conf_formats (list): Conformer formats
        structure_formats (list): Structure formats
    """
    if 'task_id' not in kwargs:
        kwargs['task_id'] = str(uuid.uuid4())
    
    task_id = kwargs['task_id']
    output_dir = 'pdf2chemicals_output'
    output_filename = str(uuid.uuid4())

    try:
        user = User.objects.get(id=kwargs['user_id'])
    except ObjectDoesNotExist:
        logger.error(f"User {kwargs['user_id']} not found")
        raise self.retry(countdown=10, max_retries=5)

    # Initialize UserTask record
    UserTask.objects.update_or_create(
        task_id=task_id,
        defaults={
            "user": user,
            "status": UserTask.TaskStatus.PENDING,
            "label": f'PDF2Chemicals: {kwargs["original_filename"]}'
        }
    )

    logger.info(f"Starting PDF2Chemicals workflow for task {task_id}")

    # Define workflow chain
    workflow = chain(
        create_pbs_script_task.s(
            pdf_path=kwargs['pdf_path'],
            export_format=kwargs['export_format'],
            conf_formats=kwargs['conf_formats'],
            structure_formats=kwargs['structure_formats'],
            output_dir=output_dir,
            output_filename=output_filename
        ),
        send_pdf2chemicals_hpc_task.s(),
        monitor_pdf2chemicals_job.s(),
        load_chemical_from_json.s(export_format=kwargs['export_format']),
        post_chemicals_in_db.s(user_id=kwargs['user_id']),
        return_pdf2chemicals_task_final_result.s(
            export_format=kwargs['export_format'],
            output_dir=output_dir,
            output_filename=output_filename,
            task_id=task_id
        )
    )

    # Apply workflow with error handler
    workflow.apply_async(
        link_error=handle_pdf2chemicals_task_error.s(
            pdf_path=kwargs['pdf_path'],
            user_id=kwargs['user_id'],
            original_filename=kwargs['original_filename'],
            export_format=kwargs['export_format'],
            conf_formats=kwargs['conf_formats'],
            structure_formats=kwargs['structure_formats'],
            task_id=task_id
        ),
        task_id=task_id
    )

    return task_id


# ============================================================================
# ERROR & REVOCATION HANDLERS
# ============================================================================

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.handle_pdf2chemicals_task_error',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks'
)
def handle_pdf2chemicals_task_error(self, *args, **kwargs):
    """
    Handle errors in main workflow.
    
    Checks task status and retries if appropriate.
    Skips retry if task was explicitly revoked.
    """
    user_id = kwargs.get('user_id')
    pdf_path = kwargs.get('pdf_path')
    original_filename = kwargs.get('original_filename')
    export_format = kwargs.get('export_format')
    conf_formats = kwargs.get('conf_formats')
    structure_formats = kwargs.get('structure_formats')
    task_id = kwargs.get('task_id', str(uuid.uuid4()))

    task = UserTask.objects.filter(task_id=task_id).first()

    if not task:
        logger.error(f"Task {task_id} not found in error handler")
        return

    # Skip retry if task was revoked
    if task.status in [UserTask.TaskStatus.REVOKED, UserTask.TaskStatus.RETRY, UserTask.TaskStatus.SUCCESS]:
        logger.info(
            f"Skipping retry for task {task_id} with status {task.status}"
        )
        return

    logger.warning(f"Retrying task {task_id} for user {user_id} in 5 minutes")

    extract_and_save_chemicals_from_pdf.apply_async(
        kwargs={
            'user_id': user_id,
            'pdf_path': pdf_path,
            'original_filename': original_filename,
            'export_format': export_format,
            'conf_formats': conf_formats,
            'structure_formats': structure_formats,
            'task_id': task_id
        },
        countdown=60 * 5
    )

    UserTask.objects.update_or_create(
        task_id=task_id,
        defaults={'status': UserTask.TaskStatus.RETRY}
    )


# ============================================================================
# WORKFLOW TASKS
# ============================================================================

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_create_pbs_script_task',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 2,
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def create_pbs_script_task(self, *args, **kwargs):
    """
    Create PBS script and reserve cluster node.
    
    ✅ REVOCATION-AWARE: Checks for revocation at start/end
    ✅ RESOURCE-SAFE: Tracks cleanup data for later deletion
    
    Returns:
        dict: Task data including cleanup_data for revocation handling
    """
    # ✅ CHECK REVOCATION AT START
    if self.check_revocation():
        logger.warning(f"Task {self.request.id} revoked before execution")
        return {
            'revoked': True,
            'task_id': self.request.id,
            'message': 'Task was revoked before execution'
        }

    output_abs_dir = os.path.join(settings.MEDIA_ROOT, kwargs['output_dir'])
    json_filepath = os.path.join(output_abs_dir, f'{kwargs["output_filename"]}.json')
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, kwargs['pdf_path'])

    cluster_node_manager = ClusterNodeManager()
    node_name = cluster_node_manager.reserve_available_gpu_node()

    if node_name == '':
        logger.error("No cluster nodes available")
        raise ResourceUnavailable("No pbs node is available at the moment.")

    reservation_id = cluster_node_manager.get_reservation_id_from_node_name(node_name)

    # ✅ TRACK CLEANUP DATA FOR REVOCATION
    cleanup_data = {
        'node_name': node_name,
        'reservation_id': reservation_id,
        'pbs_script_path': None,
        'pdf_path': absolute_pdf_path,
        'json_filepath': json_filepath,
        'task_id': self.request.id
    }

    try:
        script_path = generate_pbs_script(
            pdf_path=absolute_pdf_path,
            output_dir=output_abs_dir,
            export_format=kwargs['export_format'],
            conf_formats=kwargs['conf_formats'],
            structure_formats=kwargs['structure_formats'],
            filename=kwargs['output_filename'],
            node_name=node_name
        )

        if not file_exists(script_path):
            cluster_node_manager.mark_node_as_available(node_name)
            raise FileExistsError(f"PBS script {script_path} not found")

        if not cluster_node_manager.is_node_reservation_valid(node_name, reservation_id):
            remove_file(script_path)
            cluster_node_manager.mark_node_as_available(node_name)
            raise KeyError("Cluster node reservation id is invalid")

        cleanup_data['pbs_script_path'] = script_path

        # ✅ CHECK REVOCATION BEFORE RETURNING
        if self.check_revocation():
            logger.warning(f"Task {self.request.id} revoked, triggering cleanup")
            cleanup_pdf2chemicals_resources.apply_async(
                args=[cleanup_data],
                task_id=f"{self.request.id}-cleanup"
            )
            return {'revoked': True, 'task_id': self.request.id}

        logger.info(f"✓ PBS script created: {script_path} (node: {node_name})")

        return {
            'pbs_script_path': script_path,
            'node_name': node_name,
            'reservation_id': reservation_id,
            'json_filepath': json_filepath,
            'pdf_path': absolute_pdf_path,
            'cleanup_data': cleanup_data  # ✅ PASS TO NEXT TASK
        }

    except Exception as e:
        logger.error(f"Exception in create_pbs_script_task: {e}")
        cluster_node_manager.mark_node_as_available(node_name)
        raise


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_send_pdf2chemicals_hpc_task',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 2,
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def send_pdf2chemicals_hpc_task(self, *args, **kwargs):
    """
    Submit job to HPC cluster via PBS/TORQUE.
    
    ✅ REVOCATION-AWARE: Checks for revocation and triggers cleanup
    
    Returns:
        dict: Job submission data including cleanup_data
    """
    # ✅ CHECK REVOCATION
    if self.check_revocation():
        logger.warning(f"Task {self.request.id} revoked before HPC submission")
        cleanup_data = kwargs.get('cleanup_data', {})
        if cleanup_data:
            cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
        return {'revoked': True, 'task_id': self.request.id}

    pbs_script_path = kwargs.get('pbs_script_path')
    node_name = kwargs.get('node_name')
    reservation_id = kwargs.get('reservation_id')
    json_filepath = kwargs.get('json_filepath')
    pdf_path = kwargs.get('pdf_path')
    cleanup_data = kwargs.get('cleanup_data', {})

    cluster_node_manager = ClusterNodeManager()

    if not cluster_node_manager.is_node_reservation_valid(node_name, reservation_id):
        remove_file(pbs_script_path)
        cluster_node_manager.mark_node_as_available(node_name)
        raise KeyError("Cluster node reservation id is invalid")

    cmd = (
        f'sh -c "(cd {os.getenv("TORQUE_USER_HOME")} && '
        f'{os.getenv("TORQUE_HOME")}/bin/qsub {pbs_script_path})"'
    )

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False
    )

    if result.returncode != 0:
        remove_file(pbs_script_path)
        cluster_node_manager.mark_node_as_available(node_name)
        logger.error(f"qsub failed: {result.stderr}")
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            output=result.stdout,
            stderr=result.stderr
        )

    job_id = result.stdout.strip()
    cleanup_data['job_id'] = job_id

    logger.info(f"✓ HPC job submitted: {job_id} (node: {node_name})")

    return {
        'pbs_script_path': pbs_script_path,
        'job_id': job_id,
        'node_name': node_name,
        'json_filepath': json_filepath,
        'pdf_path': pdf_path,
        'cleanup_data': cleanup_data  # ✅ PASS TO NEXT TASK
    }


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_monitor_pdf2chemicals_job',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 5,
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def monitor_pdf2chemicals_job(self, *args, **kwargs):
    """
    Monitor HPC job completion by polling PBS queue.
    
    ✅ REVOCATION-AWARE: Checks for revocation in polling loop
    
    Returns:
        dict: JSON filepath and cleanup_data
    """
    # ✅ CHECK REVOCATION BEFORE POLLING STARTS
    if self.check_revocation():
        logger.warning(f"Task {self.request.id} revoked before monitoring")
        cleanup_data = kwargs.get('cleanup_data', {})
        if cleanup_data:
            cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
        return {'revoked': True, 'task_id': self.request.id}

    job_id = kwargs['job_id']
    cleanup_data = kwargs.get('cleanup_data', {})

    if not is_pbs_job_completed(job_id):
        # ✅ CHECK REVOCATION IN POLLING LOOP
        if self.check_revocation():
            logger.warning(f"Task {self.request.id} revoked during HPC monitoring")
            cleanup_data['job_id'] = job_id
            cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
            # Return revoked status instead of raising exception
            return {'revoked': True, 'task_id': self.request.id}

        logger.info(f"HPC job {job_id} not yet complete, retrying in {self.default_retry_delay}s")
        self.retry()

    # Job completed, perform cleanup
    cluster_node_manager = ClusterNodeManager()
    cluster_node_manager.mark_node_as_available(kwargs['node_name'])
    remove_file(kwargs['pbs_script_path'])

    if not file_exists(kwargs['json_filepath']):
        logger.error(f"JSON result file not found: {kwargs['json_filepath']}")
        cluster_node_manager.mark_node_as_available(kwargs['node_name'])
        raise FileExistsError("Json file not found. HPC job executed unsuccessfully")

    remove_file(kwargs['pdf_path'])

    logger.info(f"✓ HPC job {job_id} completed, results loaded")

    return {
        'json_filepath': kwargs['json_filepath'],
        'cleanup_data': cleanup_data
    }


@shared_task(
    base=ChainedTask,
    name='chemicals.tasks.pdf2chemicals_tasks_load_chemical_from_json',
    bind=True,
    queue='pdf2chemicals_tasks',
    priority=10,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2,
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def load_chemical_from_json(self, *args, **kwargs):
    """
    Load chemical data from JSON file.
    
    ✅ REVOCATION-AWARE: Detects revocation and stops processing
    
    Returns:
        list: Chemical data or revocation signal
    """
    # ✅ EARLY REVOCATION CHECK
    if self.check_revocation():
        logger.warning(f"Task {self.request.id} revoked before JSON loading")
        return {'revoked': True, 'task_id': self.request.id}

    json_filepath = kwargs['json_filepath']

    try:
        with open(json_filepath, mode='r') as json_file:
            chemical_list = json.load(json_file)
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {json_filepath}: {e}")
        raise

    if kwargs['export_format'] != 'json':
        remove_file(json_filepath)

    logger.info(f"✓ Loaded {len(chemical_list)} chemicals from JSON")

    return chemical_list


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_post_chemicals_in_db',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2,
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def post_chemicals_in_db(self, chemical_list, user_id):
    """
    Save chemicals to database using group of tasks.
    
    ✅ REVOCATION-AWARE: Detects revocation from previous tasks
    
    Args:
        chemical_list: Either list of chemicals or revocation dict
        user_id: User ID for database association
    """
    # ✅ CHECK IF PREVIOUS TASK WAS REVOKED
    if isinstance(chemical_list, dict) and chemical_list.get('revoked'):
        logger.warning(f"Task {self.request.id} skipped - chain was revoked")
        return {'revoked': True, 'task_id': self.request.id}

    post_chemical_group = group(
        post_chemical.s(chemical=chemical, user_id=user_id)
        for chemical in chemical_list
    )

    result = post_chemical_group.apply_async()

    logger.info(f"✓ Submitted {len(chemical_list)} chemicals for database storage")

    return result


@shared_task(
    base=BaseTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_return_pdf2chemicals_task_final_result',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2,
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def return_pdf2chemicals_task_final_result(self, *args, **kwargs):
    """
    Return final result file path.
    
    Args:
        **kwargs: Contains output_dir, output_filename, export_format, etc.
    
    Returns:
        dict: Result file path and metadata
    """
    output_relative_filepath = os.path.join(
        kwargs['output_dir'],
        f'{kwargs["output_filename"]}.{kwargs["export_format"]}'
    )
    output_abs_filepath = os.path.join(settings.MEDIA_ROOT, output_relative_filepath)

    # Update UserTask status to SUCCESS
    try:
        UserTask.objects.filter(task_id=kwargs['task_id']).update(
            status=UserTask.TaskStatus.SUCCESS
        )
        logger.info(f"✓ Task {kwargs['task_id']} marked as SUCCESS")
    except Exception as e:
        logger.error(f"Failed to update UserTask status: {e}")

    logger.info(f"✓ PDF2Chemicals workflow completed: {output_relative_filepath}")

    return {
        'result': {
            'file': output_relative_filepath,
            'format': kwargs['export_format']
        },
        'data_file': output_abs_filepath,
        'task_id': kwargs['task_id']
    }
