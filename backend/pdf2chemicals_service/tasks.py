# ============================================================================
# PDF2CHEMICALS TASK ORCHESTRATION
# ============================================================================

import os
import json
import logging
import subprocess
from uuid import uuid4

from celery import chain, group, shared_task
from django.conf import settings
from django.utils import timezone

from tasks.models import UserTask, TaskRetryTracker
from user.models import User
from tasks.util.tasks import ChainedTask, ChainedFinalTask
from chemicals.tasks import post_chemical

from .util.util import file_exists, remove_file
from .cluster import (
    ResourceUnavailable,
    ClusterNodeManager,
    generate_pbs_script,
    is_pbs_job_completed,
    cancel_hpc_job,
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
    task_reject_on_worker_lost=True,
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
    Main orchestration task - initiates entire PDF2Chemicals workflow.
    
    ✅ Creates UserTask record with PENDING status
    ✅ Builds initial message dict with all parameters
    ✅ Submits chain with proper error handler linking
    ✅ Uses same parent_task_id throughout
    
    Note: This task ONLY does orchestration.
    The actual workflow stages (create_pbs_script, send_hpc, etc.)
    are in the chain below.
    
    Args:
        user_id: User requesting processing
        pdf_path: Relative path to PDF
        original_filename: Original filename
        export_format: Output format
        conf_formats: Conformer formats
        structure_formats: Structure formats
    
    Returns:
        dict: Status of chain submission
    """
    
    parent_task_id = str(self.request.id)
    output_dir = 'pdf2chemicals_output'
    output_filename = str(uuid4())
    
    logger.info(
        f"[ORCHESTRATION] Starting PDF2Chemicals extraction "
        f"(task_id={parent_task_id}, pdf={original_filename})"
    )
    
    # ============================================
    # STEP 1: Validate user exists
    # ============================================
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"[ORCHESTRATION] User {user_id} not found")
        raise ValueError(f"User {user_id} does not exist")
    
    # ============================================
    # STEP 2: Create UserTask record
    # ============================================
    
    try:
        user_task = UserTask.objects.create(
            user=user,
            task_id=parent_task_id,
            status=UserTask.TaskStatus.PENDING,
            label=f'PDF2Chemicals: {original_filename}'
        )
        logger.info(f"[ORCHESTRATION] ✓ UserTask created: {parent_task_id}")
    except Exception as e:
        logger.error(f"[ORCHESTRATION] Failed to create UserTask: {e}")
        raise
    
    # ============================================
    # STEP 3: Build initial message
    # ============================================
    
    initial_message = {
        'status': 'pending',
        'stage': 'orchestration',
        'parent_task_id': parent_task_id,
        'user_id': user_id,
        'pdf_path': pdf_path,
        'original_filename': original_filename,
        'export_format': export_format,
        'conf_formats': conf_formats,
        'structure_formats': structure_formats,
        'output_dir': output_dir,
        'output_filename': output_filename,
        'created_at': timezone.now().isoformat(),
    }
    
    # ============================================
    # STEP 4: Build workflow chain
    # ============================================
    
    workflow = chain(
        create_pbs_script_task.s(initial_message),
        send_pdf2chemicals_hpc_task.s(),
        monitor_pdf2chemicals_job.s(),
        load_chemical_from_json.s(),
        post_chemicals_in_db.s(),
        return_pdf2chemicals_task_final_result.s(),
    )
    
    # ============================================
    # STEP 5: Submit workflow with error handler
    # ============================================
    
    try:
        # IMPORTANT: Pass entire initial_message to error handler
        # Error handler needs all this context to work properly
        workflow.apply_async(
            task_id=parent_task_id,
            link_error=handle_pdf2chemicals_task_error.s(**initial_message)
        )
        
        logger.info(
            f"[ORCHESTRATION] ✓ Workflow chain submitted "
            f"({len(workflow.tasks)} tasks in chain)"
        )
        
        return {
            'status': 'submitted',
            'stage': 'orchestration',
            'parent_task_id': parent_task_id,
            'message': 'Workflow submitted successfully'
        }
        
    except Exception as e:
        logger.error(
            f"[ORCHESTRATION] Failed to submit workflow: {e}",
            exc_info=True
        )
        
        # Mark task as failed immediately
        user_task.status = UserTask.TaskStatus.FAILURE
        user_task.error_message = f"Workflow submission failed: {str(e)}"
        user_task.save()
        
        raise


# ============================================================================
# ERROR HANDLER WITH CENTRALIZED RETRY TRACKING
# ============================================================================

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.handle_pdf2chemicals_task_error',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    reject_on_worker_lost=True,
)
def handle_pdf2chemicals_task_error(self, *args, **kwargs):
    """
    Handle errors in PDF2Chemicals workflow.
    
    ARCHITECTURE NOTES:
    
    1. This task gets a NEW task_id each time it's invoked
    2. self.request.retries is NOT reliable here (resets to 0)
    3. Solution: Use TaskRetryTracker model in database
    4. TaskRetryTracker tracks retries across error handler invocations
    
    RETRY LOGIC:
    
    First call (error handler task_id=abc):
      ├─ TaskRetryTracker(parent=xyz).increment_and_check() → 1
      ├─ if 1 < 5: schedule retry
      └─ if 1 >= 5: don't schedule retry → routes to DLQ
    
    Second call (error handler task_id=def, different!):
      ├─ TaskRetryTracker(parent=xyz).increment_and_check() → 2
      ├─ if 2 < 5: schedule retry
      └─ if 2 >= 5: don't schedule retry → routes to DLQ
    
    Fifth call:
      ├─ TaskRetryTracker(parent=xyz).increment_and_check() → 5
      ├─ if 5 < 5: FALSE
      └─ else: don't call apply_async() → message expires → DLQ
    
    DLQ ROUTING:
    
    The key: If we DON'T call workflow.apply_async(), the message
    just expires in the queue and RabbitMQ routes it to DLX (dead-letter exchange)
    configured in celery.py. It ends up in dlq_pdf2chemicals queue.
    
    ✅ Checks task revocation
    ✅ Uses TaskRetryTracker for retry count (centralized, durable)
    ✅ Re-submits workflow with SAME parent_task_id (maintains identity)
    ✅ Routes to DLQ by NOT calling apply_async() after max retries
    ✅ Cleans up resources on failure
    
    Receives: Initial message dict from chain setup + exception info
    Returns: Error status dict
    """
    
    # ============================================
    # STEP 1: Extract parameters
    # ============================================
    
    parent_task_id = kwargs.get('parent_task_id')
    user_id = kwargs.get('user_id')
    pdf_path = kwargs.get('pdf_path')
    original_filename = kwargs.get('original_filename')
    export_format = kwargs.get('export_format')
    conf_formats = kwargs.get('conf_formats', [])
    structure_formats = kwargs.get('structure_formats', [])
    output_dir = kwargs.get('output_dir')
    output_filename = kwargs.get('output_filename')
    cleanup_data = kwargs.get('cleanup_data', {})
    
    logger.error(
        f"[ERROR_HANDLER] Workflow failed: {parent_task_id}"
    )
    
    # ============================================
    # STEP 2: Get task from database
    # ============================================
    
    try:
        user_task = UserTask.objects.get(task_id=parent_task_id)
    except UserTask.DoesNotExist:
        logger.error(f"[ERROR_HANDLER] UserTask not found: {parent_task_id}")
        return {
            'status': 'error',
            'stage': 'error_handler',
            'parent_task_id': parent_task_id,
            'error': 'UserTask not found'
        }
    
    # ============================================
    # STEP 3: Check if task was revoked
    # ============================================
    
    if self.check_revocation(parent_task_id):
        logger.info(
            f"[ERROR_HANDLER] Task was revoked, cleaning up {parent_task_id}"
        )
        
        _queue_cleanup(
            parent_task_id,
            reason='revocation',
            cleanup_data=cleanup_data
        )
        
        user_task.status = UserTask.TaskStatus.REVOKED
        user_task.error_message = "Task revoked by user"
        user_task.concluded_at = timezone.now()
        user_task.save()
        
        TaskRetryTracker.cleanup(parent_task_id)
        
        return {
            'status': 'revoked',
            'stage': 'error_handler',
            'parent_task_id': parent_task_id,
            'message': 'Task revoked, cleanup triggered'
        }
    
    # ============================================
    # STEP 4: Increment centralized retry counter
    # ============================================
    
    retry_count, max_exceeded = TaskRetryTracker.increment_and_check(
        parent_task_id,
        max_retries=5
    )
    
    logger.info(
        f"[ERROR_HANDLER] Retry attempt {retry_count}/5 for {parent_task_id}"
    )
    
    # ============================================
    # STEP 5: Check if max retries exceeded
    # ============================================
    
    if max_exceeded:
        logger.critical(
            f"[ERROR_HANDLER] Max retries exceeded for {parent_task_id}, "
            f"routing to DLQ"
        )
        
        # Update UserTask to FAILURE
        user_task.status = UserTask.TaskStatus.FAILURE
        user_task.error_message = (
            f"Task failed after 5 retry attempts. Check logs and DLQ."
        )
        user_task.concluded_at = timezone.now()
        user_task.save()
        
        # Queue cleanup
        _queue_cleanup(
            parent_task_id,
            reason='failure_max_retries',
            cleanup_data=cleanup_data
        )
        
        # Clean up retry tracker
        TaskRetryTracker.cleanup(parent_task_id)
        
        # ✅ CRITICAL: Don't call apply_async()
        # This causes message to expire and route to DLQ
        
        return {
            'status': 'failed_max_retries',
            'stage': 'error_handler',
            'parent_task_id': parent_task_id,
            'message': 'Max retries exhausted, message routes to DLQ'
        }
    
    # ============================================
    # STEP 6: Schedule retry by re-submitting workflow
    # ============================================
    
    logger.warning(
        f"[ERROR_HANDLER] Scheduling retry #{retry_count}/5 "
        f"in 5 minutes for {parent_task_id}"
    )
    
    try:
        # Update UserTask to show retry status
        user_task.status = UserTask.TaskStatus.RETRY
        user_task.error_message = f"Retry attempt {retry_count}/5 scheduled"
        user_task.save()
        
        # Rebuild message for re-submission
        retry_message = {
            'status': 'retrying',
            'stage': 'error_handler_retry',
            'parent_task_id': parent_task_id,
            'user_id': user_id,
            'pdf_path': pdf_path,
            'original_filename': original_filename,
            'export_format': export_format,
            'conf_formats': conf_formats,
            'structure_formats': structure_formats,
            'output_dir': output_dir,
            'output_filename': output_filename,
            'created_at': kwargs.get('created_at'),
            'cleanup_data': cleanup_data,
        }
        
        # Re-submit workflow chain
        workflow = chain(
            create_pbs_script_task.s(retry_message),
            send_pdf2chemicals_hpc_task.s(),
            monitor_pdf2chemicals_job.s(),
            load_chemical_from_json.s(),
            post_chemicals_in_db.s(),
            return_pdf2chemicals_task_final_result.s(),
        )
        
        # ✅ IMPORTANT: Use SAME parent_task_id
        # This maintains workflow identity across retries
        workflow.apply_async(
            countdown=60 * 5,  # 5 minute delay before retry
            task_id=parent_task_id,  # ← SAME task_id!
            link_error=handle_pdf2chemicals_task_error.s(**retry_message)
        )
        
        logger.info(
            f"[ERROR_HANDLER] ✓ Retry scheduled: {parent_task_id} "
            f"(retry #{retry_count})"
        )
        
        return {
            'status': 'retry_scheduled',
            'stage': 'error_handler',
            'parent_task_id': parent_task_id,
            'retry_count': retry_count,
            'message': f'Retry #{retry_count}/5 scheduled in 5 minutes'
        }
        
    except Exception as e:
        logger.error(
            f"[ERROR_HANDLER] Failed to schedule retry: {e}",
            exc_info=True
        )
        
        # Mark as failed
        user_task.status = UserTask.TaskStatus.FAILURE
        user_task.error_message = f"Retry scheduling failed: {str(e)}"
        user_task.concluded_at = timezone.now()
        user_task.save()
        
        # Queue cleanup
        _queue_cleanup(
            parent_task_id,
            reason='failure_retry_scheduling',
            cleanup_data=cleanup_data
        )
        
        # Clean up retry tracker
        TaskRetryTracker.cleanup(parent_task_id)
        
        # Don't call apply_async() → routes to DLQ
        
        return {
            'status': 'retry_scheduling_failed',
            'stage': 'error_handler',
            'parent_task_id': parent_task_id,
            'error': str(e),
            'message': 'Retry scheduling failed, routing to DLQ'
        }


def _queue_cleanup(parent_task_id, reason='unknown', cleanup_data=None):
    """
    Queue cleanup task (idempotent and non-blocking).
    
    Cleanup happens asynchronously. If it fails, it can be retried manually.
    We don't fail the main workflow if cleanup fails.
    """
    if cleanup_data is None:
        cleanup_data = {}
    
    cleanup_data['task_id'] = parent_task_id
    cleanup_data['reason'] = reason
    
    try:
        cleanup_pdf2chemicals_resources.apply_async(
            args=[cleanup_data],
            queue='pdf2chemicals_tasks'
        )
        logger.info(
            f"[CLEANUP] Queued cleanup task for {parent_task_id} ({reason})"
        )
    except Exception as e:
        logger.error(
            f"[CLEANUP] Failed to queue cleanup: {e}",
            exc_info=True
        )
        # Don't fail - cleanup can be retried or done manually


# ============================================================================
# WORKFLOW TASKS (Chain stages)
# ============================================================================

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.create_pbs_script_task',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    max_retries=3,
    default_retry_delay=60 * 2,
)
def create_pbs_script_task(self, *args, **kwargs):
    """
    Stage 1: Create PBS script and reserve cluster node.
    
    ✅ Receives message dict from orchestration (ChainedTask merges args)
    ✅ Creates cleanup_data dict (SOURCE of cleanup data)
    ✅ Checks revocation at start and end
    ✅ Returns enhanced message with all previous data
    
    Message In: initial_message from orchestration
    Message Out: Same + pbs_script_path, node_name, reservation_id, cleanup_data
    """
    
    parent_task_id = kwargs.get('parent_task_id')
    output_dir = kwargs.get('output_dir')
    output_filename = kwargs.get('output_filename')
    pdf_path = kwargs.get('pdf_path')
    export_format = kwargs.get('export_format')
    conf_formats = kwargs.get('conf_formats', [])
    structure_formats = kwargs.get('structure_formats', [])
    
    logger.info(f"[PBS_SCRIPT] Creating PBS script for {parent_task_id}")
    
    # ============================================
    # Check revocation at entry
    # ============================================
    
    if self.check_revocation(parent_task_id):
        logger.warning(f"[PBS_SCRIPT] Revoked before script creation")
        return {
            **kwargs,
            'status': 'revoked',
            'stage': 'pbs_script',
            'revoked': True,
        }
    
    # ============================================
    # Reserve node and create script
    # ============================================
    
    try:
        output_abs_dir = os.path.join(settings.MEDIA_ROOT, output_dir)
        json_filepath = os.path.join(output_abs_dir, f'{output_filename}.json')
        absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
        
        os.makedirs(output_abs_dir, exist_ok=True)
        
        cluster_node_manager = ClusterNodeManager()
        node_name = cluster_node_manager.reserve_available_gpu_node()
        
        if not node_name or node_name == '':
            raise ResourceUnavailable("No GPU nodes available")
        
        reservation_id = cluster_node_manager.get_reservation_id_from_node_name(
            node_name
        )
        
        # Generate PBS script
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
            raise FileExistsError(f"PBS script not created: {script_path}")
        
        # Validate reservation
        if not cluster_node_manager.is_node_reservation_valid(node_name, reservation_id):
            remove_file(script_path)
            cluster_node_manager.mark_node_as_available(node_name)
            raise KeyError("Reservation invalid")
        
        logger.info(
            f"[PBS_SCRIPT] ✓ Script created at {script_path} (node: {node_name})"
        )
        
        # ============================================
        # Check revocation before returning
        # ============================================
        
        if self.check_revocation(parent_task_id):
            logger.warning("[PBS_SCRIPT] Revoked after script creation")
            cleanup_data = {
                'node_name': node_name,
                'reservation_id': reservation_id,
                'pbs_script_path': script_path,
                'json_filepath': json_filepath,
                'pdf_path': absolute_pdf_path,
            }
            _queue_cleanup(parent_task_id, 'revocation', cleanup_data)
            
            return {
                **kwargs,
                'status': 'revoked',
                'stage': 'pbs_script',
                'revoked': True,
                'cleanup_data': cleanup_data,
            }
        
        # ============================================
        # Return enhanced message
        # ============================================
        
        cleanup_data = {
            'node_name': node_name,
            'reservation_id': reservation_id,
            'pbs_script_path': script_path,
            'json_filepath': json_filepath,
            'pdf_path': absolute_pdf_path,
        }
        
        return {
            **kwargs,
            'status': 'success',
            'stage': 'pbs_script',
            'pbs_script_path': script_path,
            'node_name': node_name,
            'reservation_id': reservation_id,
            'json_filepath': json_filepath,
            'cleanup_data': cleanup_data,
        }
        
    except Exception as e:
        logger.error(f"[PBS_SCRIPT] Failed: {e}", exc_info=True)
        raise


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.send_pdf2chemicals_hpc_task',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    max_retries=3,
    default_retry_delay=60 * 2,
)
def send_pdf2chemicals_hpc_task(self, *args, **kwargs):
    """
    Stage 2: Submit PBS script to HPC cluster.
    
    ✅ Receives full message from Stage 1 (including cleanup_data)
    ✅ Enhances cleanup_data with job_id
    ✅ Checks revocation before submission
    ✅ Returns message with all data preserved
    
    Message In: Stage 1 output + pbs_script_path, cleanup_data
    Message Out: Same + job_id (added to cleanup_data)
    """
    
    parent_task_id = kwargs.get('parent_task_id')
    pbs_script_path = kwargs.get('pbs_script_path')
    cleanup_data = kwargs.get('cleanup_data', {})
    
    logger.info(f"[HPC_SUBMIT] Submitting PBS job for {parent_task_id}")
    
    if self.check_revocation(parent_task_id):
        logger.warning("[HPC_SUBMIT] Revoked before submission")
        return {
            **kwargs,
            'status': 'revoked',
            'stage': 'hpc_submit',
            'revoked': True,
        }
    
    try:
        if not file_exists(pbs_script_path):
            raise FileExistsError(f"PBS script not found: {pbs_script_path}")
        
        # Submit to cluster
        job_id = _submit_pbs_job(pbs_script_path)
        
        logger.info(f"[HPC_SUBMIT] ✓ Job {job_id} submitted successfully")
        
        # Check revocation after submission
        if self.check_revocation(parent_task_id):
            logger.warning("[HPC_SUBMIT] Revoked after submission, killing job")
            try:
                cancel_hpc_job(job_id)
            except Exception as e:
                logger.warning(f"[HPC_SUBMIT] Failed to cancel job: {e}")
            
            return {
                **kwargs,
                'status': 'revoked',
                'stage': 'hpc_submit',
                'revoked': True,
                'job_id': job_id,
            }
        
        # Enhance cleanup_data with job_id
        cleanup_data['job_id'] = job_id
        
        return {
            **kwargs,
            'status': 'success',
            'stage': 'hpc_submit',
            'job_id': job_id,
            'cleanup_data': cleanup_data,
        }
        
    except Exception as e:
        logger.error(f"[HPC_SUBMIT] Failed: {e}", exc_info=True)
        raise


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.monitor_pdf2chemicals_job',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    reject_on_worker_lost=True,
)
def monitor_pdf2chemicals_job(self, *args, **kwargs):
    """
    Stage 3: Monitor HPC job until completion.
    
    ✅ Polls job status periodically
    ✅ Checks revocation during polling
    ✅ Returns when job completes
    
    Message In: job_id from Stage 2
    Message Out: Same + job_completed confirmation
    """
    
    parent_task_id = kwargs.get('parent_task_id')
    job_id = kwargs.get('job_id')
    cleanup_data = kwargs.get('cleanup_data', {})
    
    logger.info(f"[MONITOR] Monitoring job {job_id}")
    
    try:
        max_polls = 100
        poll_count = 0
        
        while poll_count < max_polls:
            # Check revocation periodically
            if self.check_revocation(parent_task_id):
                logger.warning("[MONITOR] Revoked, killing job")
                try:
                    cancel_hpc_job(job_id)
                except Exception as e:
                    logger.warning(f"[MONITOR] Failed to cancel job: {e}")
                
                return {
                    **kwargs,
                    'status': 'revoked',
                    'stage': 'monitor',
                    'revoked': True,
                }
            
            # Check job status
            if is_pbs_job_completed(job_id):
                logger.info(f"[MONITOR] ✓ Job {job_id} completed")
                
                return {
                    **kwargs,
                    'status': 'success',
                    'stage': 'monitor',
                    'job_completed': True,
                }
            
            poll_count += 1
            wait_time = min(30 * (2 ** (poll_count // 10)), 300)
            
            logger.debug(
                f"[MONITOR] Poll {poll_count}/{max_polls}, "
                f"waiting {wait_time}s before next check"
            )
            
            # Use apply_async for internal retry with countdown
            return self.apply_async(
                countdown=wait_time,
                task_id=self.request.id
            )
        
        raise TimeoutError(
            f"Job {job_id} did not complete within {max_polls} polls"
        )
        
    except Exception as e:
        logger.error(f"[MONITOR] Failed: {e}", exc_info=True)
        raise


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.load_chemical_from_json',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    max_retries=3,
    default_retry_delay=60 * 2,
)
def load_chemical_from_json(self, *args, **kwargs):
    """
    Stage 4: Load chemical data from JSON file produced by HPC.
    
    ✅ Parses JSON output from HPC job
    ✅ Extracts chemical list
    ✅ Validates file exists before parsing
    
    Message In: json_filepath from Stage 1
    Message Out: Same + chemical_list, chemical_count
    """
    
    parent_task_id = kwargs.get('parent_task_id')
    json_filepath = kwargs.get('json_filepath')
    
    logger.info(f"[LOAD_JSON] Loading chemicals from {json_filepath}")
    
    if self.check_revocation(parent_task_id):
        logger.warning("[LOAD_JSON] Revoked")
        return {
            **kwargs,
            'status': 'revoked',
            'stage': 'load_json',
            'revoked': True,
        }
    
    try:
        # Wait for file to exist (HPC may still be writing)
        max_retries_wait = 5
        for retry in range(max_retries_wait):
            if file_exists(json_filepath):
                break
            if retry < max_retries_wait - 1:
                logger.info(
                    f"[LOAD_JSON] File not ready, waiting... (attempt {retry + 1})"
                )
                raise FileNotFoundError(
                    f"JSON file not ready: {json_filepath}"
                )
        
        # Load and parse JSON
        with open(json_filepath, 'r') as f:
            json_data = json.load(f)
        
        chemical_list = json_data.get('chemicals', [])
        
        logger.info(
            f"[LOAD_JSON] ✓ Loaded {len(chemical_list)} chemicals"
        )
        
        return {
            **kwargs,
            'status': 'success',
            'stage': 'load_json',
            'chemical_list': chemical_list,
            'chemical_count': len(chemical_list),
        }
        
    except Exception as e:
        logger.error(f"[LOAD_JSON] Failed: {e}", exc_info=True)
        raise


@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.post_chemicals_in_db',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    max_retries=3,
    default_retry_delay=60 * 2,
)
def post_chemicals_in_db(self, *args, **kwargs):
    """
    Stage 5: Post chemicals to database asynchronously.
    
    ✅ Creates group of post_chemical tasks (non-blocking)
    ✅ Returns only count, NOT group result (non-serializable)
    ✅ Chemical insertion happens in background
    
    Message In: chemical_list from Stage 4, user_id from initial
    Message Out: Same + chemical_posted_count (just the count, not list)
    
    NOTE: We return chemical_posted_count (int), NOT chemical_list.
    Chemical insertion is fire-and-forget in background.
    """
    
    parent_task_id = kwargs.get('parent_task_id')
    user_id = kwargs.get('user_id')
    chemical_list = kwargs.get('chemical_list', [])
    
    logger.info(
        f"[POST_DB] Posting {len(chemical_list)} chemicals for user {user_id}"
    )
    
    if self.check_revocation(parent_task_id):
        logger.warning("[POST_DB] Revoked")
        return {
            **kwargs,
            'status': 'revoked',
            'stage': 'post_db',
            'revoked': True,
        }
    
    try:
        # Create group of tasks for background processing
        post_chemical_tasks = group(
            post_chemical.s(chemical_data, user_id)
            for chemical_data in chemical_list
        )
        
        # Submit group to background queue (non-blocking)
        # We DON'T wait for results
        post_chemical_tasks.apply_async(queue='django_tasks')
        
        logger.info(
            f"[POST_DB] ✓ Submitted {len(chemical_list)} chemicals "
            f"to background queue"
        )
        
        return {
            **kwargs,
            'status': 'success',
            'stage': 'post_db',
            'chemical_posted_count': len(chemical_list),
            # ✅ IMPORTANT: Don't return chemical_list anymore
            # (it was causing serialization issues)
        }
        
    except Exception as e:
        logger.error(f"[POST_DB] Failed: {e}", exc_info=True)
        raise


@shared_task(
    base=ChainedFinalTask,
    name='pdf2chemicals_service.tasks.return_pdf2chemicals_task_final_result',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    max_retries=3,
    default_retry_delay=60 * 2,
)
def return_pdf2chemicals_task_final_result(self, *args, **kwargs):
    """
    Stage 6 (Final): Return result and mark task SUCCESS.
    
    ✅ Uses ChainedFinalTask base class
    ✅ on_success() hook updates UserTask to SUCCESS
    ✅ Stores file in UserTask.data_file field
    ✅ Cleans up TaskRetryTracker
    
    Message In: output_dir, output_filename, export_format
    Message Out: filepath, format for on_success() hook
    """
    
    parent_task_id = kwargs.get('parent_task_id')
    output_dir = kwargs.get('output_dir')
    output_filename = kwargs.get('output_filename')
    export_format = kwargs.get('export_format')
    chemical_posted_count = kwargs.get('chemical_posted_count', 0)
    
    logger.info(f"[FINAL] Completing task {parent_task_id}")
    
    # Handle revocation case
    if kwargs.get('revoked'):
        logger.warning("[FINAL] Task was revoked")
        try:
            user_task = UserTask.objects.get(task_id=parent_task_id)
            user_task.status = UserTask.TaskStatus.REVOKED
            user_task.concluded_at = timezone.now()
            user_task.save()
        except Exception as e:
            logger.error(f"[FINAL] Failed to mark revoked: {e}")
        
        TaskRetryTracker.cleanup(parent_task_id)
        
        return {
            'status': 'revoked',
            'stage': 'final',
            'parent_task_id': parent_task_id,
        }
    
    try:
        # Construct output file path
        output_filepath = os.path.join(
            output_dir,
            f'{output_filename}.{export_format}'
        )
        
        absolute_path = os.path.join(
            settings.MEDIA_ROOT,
            output_filepath
        )
        
        # Verify file exists
        if not file_exists(absolute_path):
            raise FileNotFoundError(f"Output file not found: {absolute_path}")
        
        logger.info(f"[FINAL] ✓ Result file ready: {output_filepath}")
        
        # Clean up retry tracker (task succeeded)
        TaskRetryTracker.cleanup(parent_task_id)
        
        # Return message for ChainedFinalTask.on_success() hook
        # on_success() will:
        # 1. Read file from filepath
        # 2. Store in UserTask.data_file
        # 3. Update UserTask.status = SUCCESS
        return {
            'status': 'success',
            'stage': 'final',
            'parent_task_id': parent_task_id,
            'filepath': output_filepath,
            'format': export_format,
            'chemical_count': chemical_posted_count,
        }
        
    except Exception as e:
        logger.error(f"[FINAL] Failed: {e}", exc_info=True)
        raise


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _submit_pbs_job(pbs_script_path):
    """
    Submit PBS script to cluster and return job ID.
    
    Args:
        pbs_script_path: Path to PBS script file
    
    Returns:
        str: Job ID returned by qsub
    
    Raises:
        subprocess.CalledProcessError: If qsub fails
    """
    result = subprocess.run(
        ['qsub', pbs_script_path],
        capture_output=True,
        text=True,
        check=True
    )
    job_id = result.stdout.strip()
    return job_id
