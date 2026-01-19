"""
PDF2Chemicals main task orchestration with revocation support.

All tasks check UserTask.status == REVOKED and propagate parent_task_id
through the chain to enable distributed revocation handling.

Key fixes:
- ✅ All tasks use .get() for safe parameter extraction
- ✅ All tasks propagate ALL parameters even when revoked
- ✅ JSON cleanup on revocation before returning
- ✅ No KeyError on early revocation
- ✅ Comprehensive logging and resource cleanup
- ✅ post_chemicals_in_db and return_pdf2chemicals_task_final_result use (self, *args, **kwargs)
"""

import os
import json
import subprocess
import uuid
import logging
from datetime import datetime
from celery import chain, group, shared_task
from celery.result import AsyncResult
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

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
    is_pbs_job_completed,
    cancel_hpc_job
)
from .cleanup import cleanup_pdf2chemicals_resources

logger = logging.getLogger(__name__)


# ============================================================================
# MAIN ORCHESTRATION TASK
# ============================================================================


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.extract_and_save_chemicals_from_pdf',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    autoretry_for=(Exception,),
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def extract_and_save_chemicals_from_pdf(
    self,
    user_id,
    pdf_path,
    original_filename,
    export_format,
    conf_formats,
    structure_formats
):
    """
    Main orchestration task for PDF2Chemicals extraction.
    
    Creates a chain: PBS script → HPC submit → Monitor → Load → Save → Return result
    
    ✅ Creates UserTask record with RUNNING status
    ✅ Passes parent_task_id to all child tasks
    ✅ Child tasks check UserTask.status == REVOKED
    
    Args:
        user_id (int): User requesting the processing
        pdf_path (str): Relative path to PDF in MEDIA_ROOT
        original_filename (str): Original PDF filename
        export_format (str): Output format (json, sdf, mol, etc.)
        conf_formats (list): Conformer formats
        structure_formats (list): Structure formats
    
    Returns:
        str: Parent task ID for tracking
    """
    parent_task_id = self.request.id
    output_dir = 'pdf2chemicals_output'
    output_filename = str(uuid.uuid4())
    
    logger.info(f"Starting PDF extraction (task_id={parent_task_id})")
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        raise self.retry(countdown=10, max_retries=5)
    
    # ✅ Create UserTask record
    pdf_task, _ = UserTask.objects.update_or_create(
        task_id=parent_task_id,
        defaults={
            "user": user,
            "status": UserTask.TaskStatus.RUNNING,
            "label": f'PDF2Chemicals: {original_filename}'
        }
    )
    
    logger.info(f"✓ UserTask created: {parent_task_id}")
    
    try:
        # ✅ CHECK REVOCATION BEFORE STARTING CHAIN
        if self.check_revocation(parent_task_id):
            pdf_task.mark_revoked()
            return {'status': 'revoked', 'stage': 'start'}
        
        # Define workflow chain
        workflow = chain(
            create_pbs_script_task.s(
                pdf_path=pdf_path,
                export_format=export_format,
                conf_formats=conf_formats,
                structure_formats=structure_formats,
                output_dir=output_dir,
                output_filename=output_filename,
                parent_task_id=parent_task_id  # ← Pass parent ID
            ),
            send_pdf2chemicals_hpc_task.s(parent_task_id=parent_task_id),
            monitor_pdf2chemicals_job.s(parent_task_id=parent_task_id),
            load_chemical_from_json.s(parent_task_id=parent_task_id),
            post_chemicals_in_db.s(user_id=user_id, parent_task_id=parent_task_id),
            return_pdf2chemicals_task_final_result.s(
                export_format=export_format,
                output_dir=output_dir,
                output_filename=output_filename,
                task_id=parent_task_id,
                parent_task_id=parent_task_id
            )
        )
        
        # Apply workflow
        workflow.apply_async(
            link_error=handle_pdf2chemicals_task_error.s(
                user_id=user_id,
                pdf_path=pdf_path,
                original_filename=original_filename,
                export_format=export_format,
                conf_formats=conf_formats,
                structure_formats=structure_formats,
                task_id=parent_task_id
            ),
            task_id=parent_task_id
        )
        
        return str(parent_task_id)
    
    except Exception as e:
        logger.error(f"Error in orchestration: {e}", exc_info=True)
        pdf_task.status = UserTask.TaskStatus.FAILURE
        pdf_task.error_message = str(e)
        pdf_task.save()
        raise


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
    
    Args:
        **kwargs: user_id, pdf_path, original_filename, task_id, etc.
    """
    user_id = kwargs.get('user_id')
    pdf_path = kwargs.get('pdf_path')
    original_filename = kwargs.get('original_filename')
    export_format = kwargs.get('export_format')
    conf_formats = kwargs.get('conf_formats')
    structure_formats = kwargs.get('structure_formats')
    task_id = kwargs.get('task_id')
    
    task = UserTask.objects.filter(task_id=task_id).first()
    
    if not task:
        logger.error(f"Task {task_id} not found in error handler")
        return
    
    # ✅ Skip retry if task was revoked
    if task.status == UserTask.TaskStatus.REVOKED:
        logger.info(f"Skipping retry for revoked task {task_id}")
        return
    
    # Skip retry if already succeeded or in retry state
    if task.status in [UserTask.TaskStatus.SUCCESS, UserTask.TaskStatus.RETRY]:
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
            'structure_formats': structure_formats
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
    name='pdf2chemicals_service.tasks.create_pbs_script_task',
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
    
    ✅ Checks UserTask.status == REVOKED at start and end
    ✅ Tracks cleanup data for revocation handling
    ✅ Passes parent_task_id and all parameters to next task
    ✅ Uses safe .get() extraction
    
    Returns:
        dict: Task data including cleanup_data and parent_task_id
    """
    parent_task_id = kwargs.get('parent_task_id')
    
    # ✅ CHECK REVOCATION BEFORE EXECUTION
    if self.check_revocation(parent_task_id):
        logger.warning(f"Revoked before PBS script creation")
        return {'revoked': True, 'parent_task_id': parent_task_id}
    
    # ✅ Safe parameter extraction
    output_dir = kwargs.get('output_dir')
    output_filename = kwargs.get('output_filename')
    pdf_path = kwargs.get('pdf_path')
    export_format = kwargs.get('export_format')
    conf_formats = kwargs.get('conf_formats')
    structure_formats = kwargs.get('structure_formats')
    
    output_abs_dir = os.path.join(settings.MEDIA_ROOT, output_dir)
    json_filepath = os.path.join(output_abs_dir, f'{output_filename}.json')
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    
    cluster_node_manager = ClusterNodeManager()
    node_name = cluster_node_manager.reserve_available_gpu_node()
    
    if node_name == '':
        logger.error("No cluster nodes available")
        raise ResourceUnavailable("No pbs node is available at the moment.")
    
    reservation_id = cluster_node_manager.get_reservation_id_from_node_name(node_name)
    
    # Track cleanup data
    cleanup_data = {
        'node_name': node_name,
        'reservation_id': reservation_id,
        'pbs_script_path': None,
        'pdf_path': absolute_pdf_path,
        'json_filepath': json_filepath,
    }
    
    try:
        script_path = generate_pbs_script(
            pdf_path=absolute_pdf_path,
            output_dir=output_abs_dir,
            export_format=export_format,
            conf_formats=conf_formats,
            structure_formats=structure_formats,
            filename=output_filename,
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
        if self.check_revocation(parent_task_id):
            logger.warning(f"Revoked after script creation, triggering cleanup")
            cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
            # ✅ Return with ALL parameters for next task
            return {
                'revoked': True,
                'parent_task_id': parent_task_id,
                'json_filepath': json_filepath,
                'export_format': export_format,
                'cleanup_data': cleanup_data
            }
        
        logger.info(f"✓ PBS script created: {script_path} (node: {node_name})")
        
        return {
            'pbs_script_path': script_path,
            'node_name': node_name,
            'reservation_id': reservation_id,
            'json_filepath': json_filepath,
            'pdf_path': absolute_pdf_path,
            'export_format': export_format,
            'cleanup_data': cleanup_data,
            'parent_task_id': parent_task_id
        }
    
    except Exception as e:
        logger.error(f"Exception in create_pbs_script_task: {e}")
        cluster_node_manager.mark_node_as_available(node_name)
        raise


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.send_pdf2chemicals_hpc_task',
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
    
    ✅ Checks UserTask.status == REVOKED
    ✅ Kills HPC job if revoked after submission
    ✅ Propagates all parameters on revocation
    ✅ Safe parameter extraction with .get()
    """
    parent_task_id = kwargs.get('parent_task_id')
    
    # ✅ CHECK REVOCATION
    if self.check_revocation(parent_task_id):
        logger.warning(f"Revoked before HPC submission")
        cleanup_data = kwargs.get('cleanup_data', {})
        if cleanup_data:
            cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
        
        # ✅ Return with ALL parameters for next task
        return {
            'revoked': True,
            'parent_task_id': parent_task_id,
            'json_filepath': kwargs.get('json_filepath'),
            'export_format': kwargs.get('export_format'),
            'cleanup_data': kwargs.get('cleanup_data', {})
        }
    
    # ✅ Safe parameter extraction
    pbs_script_path = kwargs.get('pbs_script_path')
    node_name = kwargs.get('node_name')
    reservation_id = kwargs.get('reservation_id')
    json_filepath = kwargs.get('json_filepath')
    pdf_path = kwargs.get('pdf_path')
    export_format = kwargs.get('export_format')
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
            result.returncode, cmd, output=result.stdout, stderr=result.stderr
        )
    
    job_id = result.stdout.strip()
    cleanup_data['job_id'] = job_id
    
    # ✅ CHECK REVOCATION AFTER SUBMISSION
    if self.check_revocation(parent_task_id):
        logger.warning(f"Revoked after submission, killing job {job_id}")
        cancel_hpc_job(job_id)
        cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
        # ✅ Return with ALL parameters for next task
        return {
            'revoked': True,
            'parent_task_id': parent_task_id,
            'json_filepath': json_filepath,
            'export_format': export_format,
            'cleanup_data': cleanup_data
        }
    
    logger.info(f"✓ HPC job submitted: {job_id}")
    
    return {
        'pbs_script_path': pbs_script_path,
        'job_id': job_id,
        'node_name': node_name,
        'json_filepath': json_filepath,
        'pdf_path': pdf_path,
        'export_format': export_format,
        'cleanup_data': cleanup_data,
        'parent_task_id': parent_task_id
    }


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.monitor_pdf2chemicals_job',
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
    
    ✅ Checks UserTask.status == REVOKED in polling loop
    ✅ Kills job if revoked during monitoring
    ✅ Propagates all parameters on revocation
    ✅ Safe parameter extraction with .get()
    """
    parent_task_id = kwargs.get('parent_task_id')
    job_id = kwargs.get('job_id')
    cleanup_data = kwargs.get('cleanup_data', {})
    json_filepath = kwargs.get('json_filepath')
    export_format = kwargs.get('export_format')
    node_name = kwargs.get('node_name')
    pbs_script_path = kwargs.get('pbs_script_path')
    pdf_path = kwargs.get('pdf_path')
    
    # ✅ CHECK REVOCATION BEFORE POLLING STARTS
    if self.check_revocation(parent_task_id):
        logger.warning(f"Revoked before monitoring job {job_id}")
        cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
        # ✅ Return with ALL parameters for next task
        return {
            'revoked': True,
            'parent_task_id': parent_task_id,
            'json_filepath': json_filepath,
            'export_format': export_format,
            'cleanup_data': cleanup_data
        }
    
    if not is_pbs_job_completed(job_id):
        # ✅ CHECK REVOCATION IN POLLING LOOP
        if self.check_revocation(parent_task_id):
            logger.warning(f"Revoked during monitoring, killing job {job_id}")
            cancel_hpc_job(job_id)
            cleanup_data['job_id'] = job_id
            cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
            # ✅ Return with ALL parameters for next task
            return {
                'revoked': True,
                'parent_task_id': parent_task_id,
                'json_filepath': json_filepath,
                'export_format': export_format,
                'cleanup_data': cleanup_data
            }
        
        logger.info(f"Job {job_id} not complete, retrying in {self.default_retry_delay}s")
        self.retry()
    
    # Job completed
    cluster_node_manager = ClusterNodeManager()
    cluster_node_manager.mark_node_as_available(node_name)
    remove_file(pbs_script_path)
    
    if not file_exists(json_filepath):
        logger.error(f"JSON result file not found: {json_filepath}")
        cluster_node_manager.mark_node_as_available(node_name)
        raise FileExistsError("Json file not found. HPC job executed unsuccessfully")
    
    remove_file(pdf_path)
    
    logger.info(f"✓ HPC job {job_id} completed")
    
    return {
        'json_filepath': json_filepath,
        'export_format': export_format,
        'cleanup_data': cleanup_data,
        'parent_task_id': parent_task_id
    }


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.load_chemical_from_json',
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
    
    ✅ Checks UserTask.status == REVOKED before loading\n
    ✅ Cleanup JSON file on revocation before returning\n
    ✅ Safe parameter extraction with .get()\n
    ✅ Propagates all parameters on revocation\n
    
    Args:
        **kwargs: json_filepath, export_format, parent_task_id
    
    Returns:
        dict: chemical_list and parent_task_id (or revocation signal)
    """
    parent_task_id = kwargs.get('parent_task_id')
    json_filepath = kwargs.get('json_filepath')
    export_format = kwargs.get('export_format')
    
    # ✅ CHECK REVOCATION BEFORE PROCESSING
    if self.check_revocation(parent_task_id):
        logger.warning(f"Revoked, enqueuing cleanup")
        
        # Pass cleanup data to background cleanup task
        cleanup_data = {
            'json_filepath': json_filepath,
            'export_format': export_format
        }
        cleanup_pdf2chemicals_resources.apply_async(args=[cleanup_data])
        
        return {'revoked': True, 'parent_task_id': parent_task_id}
    
    # ✅ Validate we have json_filepath
    if not json_filepath:
        logger.error(f"Missing json_filepath in kwargs")
        raise ValueError("json_filepath is required")
    
    try:
        with open(json_filepath, mode='r') as json_file:
            chemical_list = json.load(json_file)
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {json_filepath}: {e}")
        raise
    
    if export_format != 'json':
        remove_file(json_filepath)
    
    logger.info(f"✓ Loaded {len(chemical_list)} chemicals from JSON")
    
    return {
        'chemical_list': chemical_list,
        'parent_task_id': parent_task_id
    }


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.post_chemicals_in_db',
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
def post_chemicals_in_db(self, *args, **kwargs):
    """
    Save chemicals to database using group of tasks.
    
    ✅ Detects revocation from previous task
    ✅ Returns count instead of group result (JSON serializable)
    ✅ Safe parameter extraction with .get()
    ✅ Uses (self, *args, **kwargs) signature for chain compatibility
    
    Args:
        *args: result_data from previous task (load_chemical_from_json)
        **kwargs: user_id, parent_task_id
    
    Returns:
        dict: chemical_count and parent_task_id (or revocation signal)
    """
    # Extract from args (chain passes result_data as first arg)
    result_data = args if args else {}
    user_id = kwargs.get('user_id')
    parent_task_id = kwargs.get('parent_task_id')
    
    # ✅ CHECK IF PREVIOUS TASK WAS REVOKED
    if isinstance(result_data, dict) and result_data.get('revoked'):
        logger.warning(f"Skipped - chain was revoked")
        return {'revoked': True, 'parent_task_id': parent_task_id}
    
    # ✅ CHECK REVOCATION BEFORE PROCESSING
    if self.check_revocation(parent_task_id):
        logger.warning(f"Revoked before posting chemicals")
        return {'revoked': True, 'parent_task_id': parent_task_id}
    
    # Extract chemical list
    chemical_list = result_data.get('chemical_list', [])
    
    if not chemical_list:
        logger.warning(f"No chemicals to post")
        return {
            'chemical_count': 0,
            'parent_task_id': parent_task_id
        }
    
    # ✅ POST CHEMICALS BUT RETURN COUNT (not group result)
    # Group applies async, we just count and return
    post_chemical_group = group(
        post_chemical.s(chemical=chemical, user_id=user_id)
        for chemical in chemical_list
    )
    
    # Don't store the group result - return count instead
    post_chemical_group.apply_async()
    
    logger.info(f"✓ Submitted {len(chemical_list)} chemicals for database storage")
    
    return {
        'chemical_count': len(chemical_list),
        'parent_task_id': parent_task_id
    }


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.return_pdf2chemicals_task_final_result',
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
    Return final result file path and mark task as SUCCESS.
    
    ✅ Receives chemical_count from previous task (JSON serializable)\n
    ✅ Updates UserTask to SUCCESS\n
    ✅ Safe parameter extraction with .get()\n
    ✅ Uses (self, *args, **kwargs) signature for chain compatibility\n
    
    Args:
        *args: chemical_count_data from previous task (post_chemicals_in_db)
        **kwargs: output_dir, output_filename, export_format, task_id, parent_task_id
    
    Returns:
        dict: Final result with file path and metadata
    """
    # Extract from args (chain passes chemical_count_data as first arg)
    chemical_count_data = args if args else {}
    
    # ✅ CHECK IF PREVIOUS TASK WAS REVOKED
    if isinstance(chemical_count_data, dict) and chemical_count_data.get('revoked'):
        logger.warning(f"Revoked before final result")
        task_id = kwargs.get('task_id')
        if task_id:
            try:
                user_task = UserTask.objects.get(task_id=task_id)
                user_task.status = UserTask.TaskStatus.REVOKED
                user_task.concluded_at = timezone.now()
                user_task.save()
                logger.info(f"✓ Task {task_id} marked as REVOKED")
            except Exception as e:
                logger.error(f"Failed to update revoked task: {e}")
        return {'revoked': True}
    
    # ✅ Safe parameter extraction
    parent_task_id = kwargs.get('parent_task_id')
    task_id = kwargs.get('task_id')
    output_dir = kwargs.get('output_dir')
    output_filename = kwargs.get('output_filename')
    export_format = kwargs.get('export_format')
    
    # Validate required parameters
    if not all([task_id, output_dir, output_filename, export_format]):
        logger.error(f"Missing required parameters in final result task")
        raise ValueError("task_id, output_dir, output_filename, export_format are required")
    
    output_relative_filepath = os.path.join(
        output_dir,
        f'{output_filename}.{export_format}'
    )
    output_abs_filepath = os.path.join(settings.MEDIA_ROOT, output_relative_filepath)
    
    # ✅ UPDATE UserTask STATUS TO SUCCESS
    try:
        user_task = UserTask.objects.get(task_id=task_id)
        user_task.status = UserTask.TaskStatus.SUCCESS
        user_task.result = {
            'file': output_relative_filepath,
            'format': export_format,
            'chemical_count': chemical_count_data.get('chemical_count', 0)
        }
        user_task.concluded_at = timezone.now()
        user_task.save()
        logger.info(f"✓ Task {task_id} marked as SUCCESS")
    except Exception as e:
        logger.error(f"Failed to update UserTask: {e}")
        raise
    
    logger.info(f"✓ PDF2Chemicals workflow completed: {output_relative_filepath}")
    
    return {
        'status': 'success',
        'file': output_relative_filepath,
        'format': export_format,
        'task_id': str(task_id)
    }
