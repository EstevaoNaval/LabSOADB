import logging

from celery import shared_task

from .cluster import ClusterNodeManager, cancel_hpc_job
from .util.util import remove_file, file_exists

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
    Cleanup resources on revocation or error.
    
    Handles all file types:
    - JSON files
    - PBS scripts
    - PDFs
    - HPC nodes
    """
    
    # Clean JSON file
    json_filepath = cleanup_data.get('json_filepath')
    if json_filepath and file_exists(json_filepath):
        try:
            remove_file(json_filepath)
            logger.info(f"✓ Cleaned up JSON: {json_filepath}")
        except Exception as e:
            logger.warning(f"Failed to cleanup JSON: {e}")
    
    # Clean PBS script
    pbs_script = cleanup_data.get('pbs_script_path')
    if pbs_script and file_exists(pbs_script):
        try:
            remove_file(pbs_script)
            logger.info(f"✓ Cleaned up PBS script: {pbs_script}")
        except Exception as e:
            logger.warning(f"Failed to cleanup PBS: {e}")
    
    # Clean PDF
    pdf_path = cleanup_data.get('pdf_path')
    if pdf_path and file_exists(pdf_path):
        try:
            remove_file(pdf_path)
            logger.info(f"✓ Cleaned up PDF: {pdf_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup PDF: {e}")
    
    # Release cluster node
    node_name = cleanup_data.get('node_name')
    if node_name:
        try:
            cluster_node_manager = ClusterNodeManager()
            cluster_node_manager.mark_node_as_available(node_name)
            logger.info(f"✓ Released node: {node_name}")
        except Exception as e:
            logger.warning(f"Failed to release node: {e}")
    
    # Kill HPC job
    job_id = cleanup_data.get('job_id')
    if job_id:
        try:
            cancel_hpc_job(job_id)
            logger.info(f"✓ Killed job: {job_id}")
        except Exception as e:
            logger.warning(f"Failed to kill job: {e}")
    
    logger.info(f"✓ Cleanup completed for revoked task")
