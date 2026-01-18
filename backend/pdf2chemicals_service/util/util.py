import os
import random
import string
import logging

logger = logging.getLogger(__name__)

def generate_random_alphanumeric_sequence(size: int = 10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(size))

def file_exists(file_path):
    """Check if file exists (safely handles None)"""
    if file_path is None:
        logger.warning("file_exists called with None path")
        return False
    
    if not isinstance(file_path, (str, bytes, os.PathLike)):
        logger.error(f"Invalid path type: {type(file_path).__name__}")
        return False
    
    try:
        return os.path.exists(file_path)
    except (OSError, TypeError) as e:
        logger.error(f"Error checking file {file_path}: {e}")
        return False


def remove_file(file_path):
    """Remove file (safely handles None and all errors)"""
    if file_path is None:
        logger.warning("remove_file called with None path - skipping")
        return False
    
    if not isinstance(file_path, (str, bytes, os.PathLike)):
        logger.error(f"Invalid path type: {type(file_path).__name__}")
        return False
    
    if not file_exists(file_path):
        logger.info(f"File does not exist: {file_path}")
        return False
    
    try:
        os.remove(file_path)
        logger.info(f"✓ File removed: {file_path}")
        return True
    except FileNotFoundError:
        logger.info(f"File disappeared before deletion: {file_path}")
        return False
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        return False
    except Exception as e:
        logger.error(f"Error removing {file_path}: {e}")
        return False