import logging

from celery import shared_task

from pdf2chemicals_service.cleanup.cleanup_helpers import (
    release_gpu_node,
    cancel_hpc_job,
    remove_files,
)

logger = logging.getLogger(__name__)


@shared_task(
    name="pdf2chemicals_service.tasks.cleanup_pdf2chemicals_resources",
    bind=True,
    acks_late=True,
    queue="pdf2chemicals_tasks",
    max_retries=3,
    default_retry_delay=30,
)
def cleanup_pdf2chemicals_resources(self, cleanup_data):
    """
    Cleanup resources on revocation or error.

    Handles all file types:
    - JSON files
    - PBS scripts
    - PDFs
    - HPC TORQUE nodes
    - HPC TORQUE Job
    """

    # Clean JSON file
    json_filepath = cleanup_data.get("json_filepath")
    remove_files(json_filepath)

    # Clean PBS script
    pbs_script = cleanup_data.get("pbs_script_path")
    remove_files(pbs_script)

    # Clean PDF
    pdf_path = cleanup_data.get("pdf_path")
    remove_files(pdf_path)

    # Release cluster node
    node_name = cleanup_data.get("node_name")
    release_gpu_node(node_name)

    # Kill HPC job
    job_id = cleanup_data.get("job_id")
    cancel_hpc_job(job_id)

    logger.info(f"[CLEANUP] Cleanup completed for revoked task")
