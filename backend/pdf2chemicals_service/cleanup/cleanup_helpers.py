import logging

from pdf2chemicals_service.cluster import ClusterNodeManager, cancel_hpc_job
from pdf2chemicals_service.util.util import remove_file, file_exists


logger = logging.getLogger(__name__)


def release_gpu_node(node_name):
    """Release GPU node to available pool."""
    if not node_name:
        return False
    
    try:
        cluster_manager = ClusterNodeManager()
        cluster_manager.mark_node_as_available(node_name)
        logger.info(f"[CLEANUP] GPU node {node_name} released")
        return True
    except Exception as e:
        logger.error(f"[CLEANUP] Failed to release GPU {node_name}: {e}")
        return False


def cancel_hpc_job(job_id):
    """Cancel running HPC job."""
    if not job_id:
        return False
    
    try:
        cancel_hpc_job(job_id)
        logger.info(f"[CLEANUP] HPC job {job_id} cancelled")
        return True
    except Exception as e:
        logger.error(f"[CLEANUP] Failed to cancel job {job_id}: {e}")
        return False


def remove_files(*file_paths):
    """Remove multiple files."""
    if not file_paths:
        return True
    
    success = True
    for filepath in file_paths:
        if not filepath or not file_exists(filepath):
            continue
        
        try:
            remove_file(filepath)
            logger.info(f"[CLEANUP] Removed {filepath}")
        except Exception as e:
            logger.error(f"[CLEANUP] Failed to remove {filepath}: {e}")
            success = False
    
    return success