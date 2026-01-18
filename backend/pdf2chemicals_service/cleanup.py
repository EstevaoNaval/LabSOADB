import os
import logging
from celery import shared_task
from django.conf import settings
from tasks.models import UserTask
from .cluster import ClusterNodeManager
from .util.util import remove_file

logger = logging.getLogger(__name__)


@shared_task(
    name='pdf2chemicals_service.tasks.cleanup_pdf2chemicals_resources',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks',
    max_retries=3,
    default_retry_delay=30
)
def cleanup_pdf2chemicals_resources(self, cleanup_data):
    """
    Dedicated cleanup task for revocation scenarios.
    
    Handles release of cluster resources and deletion of temporary files.
    
    Args:
        cleanup_data (dict): Dictionary containing:
            - node_name (str): Cluster node to release
            - reservation_id (str): Reservation ID to validate
            - pbs_script_path (str): PBS script file to delete
            - pdf_path (str): PDF file to delete
            - json_filepath (str): JSON result file to delete
            - job_id (str, optional): HPC job ID if submitted
            - task_id (str): Celery task ID for tracking
    
    Returns:
        dict: Cleanup status report
    """
    if not cleanup_data:
        logger.warning('cleanup_pdf2chemicals_resources called with empty data')
        return {'cleanup': 'skipped', 'reason': 'no cleanup data'}
    
    task_id = cleanup_data.get('task_id', 'unknown')
    cleanup_report = {
        'task_id': task_id,
        'node_released': False,
        'files_deleted': [],
        'errors': []
    }
    
    cluster_node_manager = ClusterNodeManager()
    
    # Step 1: Release cluster node (CRITICAL - prevents starvation)
    if cleanup_data.get('node_name'):
        try:
            cluster_node_manager.mark_node_as_available(
                cleanup_data['node_name']
            )
            cleanup_report['node_released'] = True
            logger.info(
                f"✓ Released cluster node {cleanup_data['node_name']} "
                f"(task: {task_id})"
            )
        except Exception as e:
            error_msg = (
                f"Failed to release node {cleanup_data['node_name']}: {e}"
            )
            logger.error(error_msg)
            cleanup_report['errors'].append(error_msg)
    
    # Step 2: Delete temporary files
    file_keys = ['pbs_script_path', 'pdf_path', 'json_filepath']
    for file_key in file_keys:
        if cleanup_data.get(file_key):
            file_path = cleanup_data[file_key]
            try:
                if os.path.exists(file_path):
                    remove_file(file_path)
                    cleanup_report['files_deleted'].append(file_path)
                    logger.info(f"✓ Deleted {file_key}: {file_path}")
            except Exception as e:
                error_msg = f"Failed to delete {file_key}: {e}"
                logger.warning(error_msg)
                cleanup_report['errors'].append(error_msg)
    
    # Step 3: Update UserTask status to REVOKED
    try:
        UserTask.objects.filter(task_id=task_id).update(
            status=UserTask.TaskStatus.REVOKED
        )
        logger.info(f"✓ Updated UserTask {task_id} status to REVOKED")
    except Exception as e:
        error_msg = f"Failed to update UserTask {task_id}: {e}"
        logger.error(error_msg)
        cleanup_report['errors'].append(error_msg)
    
    # Log final report
    if cleanup_report['errors']:
        logger.warning(
            f"Cleanup completed for {task_id} with errors: "
            f"{cleanup_report['errors']}"
        )
    else:
        logger.info(f"✓ Cleanup completed successfully for {task_id}")
    
    return cleanup_report
