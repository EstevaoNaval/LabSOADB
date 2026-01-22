import os
import logging

from django.utils import timezone
from django.core.files import File

from celery.contrib.abortable import AbortableTask
from celery import current_app
from celery.result import AsyncResult

from tasks.models import UserTask


logger = logging.getLogger(__name__)

class BaseAbortableTask(AbortableTask):
    abstract = True
    
    
    
    def check_revocation(self, task_id=None):
        """
        Check if task is revoked via UserTask.status field.
        
        Args:
            task_id (str, optional): Task ID to check. 
                                    Defaults to current task ID.
        
        Returns:
            bool: True if task status is REVOKED
        
        Example:
            if self.check_revocation(parent_task_id):
                logger.warning("Task was revoked")
                return {'revoked': True}
        """
        check_id = task_id or str(self.request.id)
        
        try:
            user_task = UserTask.objects.get(task_id=check_id)
            is_revoked = user_task.status == UserTask.TaskStatus.REVOKED
            
            if is_revoked:
                logger.warning(
                    f"Task {check_id} is revoked (status={user_task.status})"
                )
            
            return is_revoked
        
        except UserTask.DoesNotExist:
            logger.warning(f"UserTask not found for {check_id}")
            return False
        except Exception as e:
            logger.error(f"Error checking revocation for {check_id}: {e}")
            return False
    
    

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Called when task fails with exception.
        Triggers cleanup for resource-intensive tasks.
        """
        logger.error(f'Task {task_id} failed: {exc}')
        self._perform_cleanup(task_id, kwargs, status='FAILED')
        
        UserTask.objects.update_or_create(
            task_id=task_id, 
            defaults={
                'status': UserTask.TaskStatus.FAILURE,
                'result': { 'error': str(exc) },
                'error_message': str(exec),
                'traceback': exec,
                'concluded_at': timezone.now()
            }
        )
        
        return super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        Called after task execution (success, failure, revocation).
        Use this to detect revocation after task completes.
        """
        try:
            user_task = UserTask.objects.filter(task_id=task_id).first()
            
            # If explicitly revoked, trigger cleanup
            if user_task and user_task.is_revoked and status != 'REVOKED':
                logger.warning(f'Cleaning up revoked task {task_id}')
                self._perform_cleanup(task_id, kwargs, status='REVOKED')
        except Exception as e:
            logger.error(f'Error in after_return for {task_id}: {e}')
    
    def _perform_cleanup(self, task_id, kwargs, status='REVOKED'):
        """
        Hook point for subclasses to implement specific cleanup.
        Override in subclasses that need custom cleanup logic.
        
        Args:
            task_id: Celery task ID
            kwargs: Original task kwargs (may contain resource info)
            status: Cleanup trigger reason (REVOKED, FAILED, etc.)
        
        Default: Does nothing. Override in subclass.
        """
        pass

class ChainedTask(BaseAbortableTask):
    """
    Enhanced base class combining:
    - AbortableTask for graceful abortion
    - ChainedTask behavior for parameter passing
    - Revocation awareness via UserTask model
    
    Features:
    - Automatic revocation checking
    - Cleanup hooks for resource management
    - Integrated with Django UserTask model
    """
    abstract = True
    
    def __call__(self, *args, **kwargs):
        """
        Merge dict args into kwargs (your ChainedTask pattern).
        Allows tasks to pass data through chain as single dict.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = ()
        return super(ChainedTask, self).__call__(*args, **kwargs)
    

class ChainedFinalTask(ChainedTask):
    abstract = True
    
    def _get_file_field_from_path(self, path):
        data_filename = os.path.basename(path)
        f = open(path, 'rb')
        return File(f, name=data_filename)
    
    def on_success(self, retval, task_id, args, kwargs):
        format = retval.get('format', {})
        filepath = retval.get('filepath', None)
        parent_task_id = retval.get('parent_task_id', None)
        
        data_file = self._get_file_field_from_path(filepath) if filepath else None
        
        result = {
            'file': data_file,
            'format': format
        }
        
        user_task_defaults = {
            'status': UserTask.TaskStatus.SUCCESS,
            'concluded_at': timezone.now(),
            'result': result,
            'data_file': data_file
        }
                
        # Atualiza o registro do UserTask com status SUCCESS e o resultado retornado
        UserTask.objects.update_or_create(
            task_id=parent_task_id,
            defaults=user_task_defaults
        )
        
        if data_file:
            data_file.close()
        
        return super().on_success(retval, task_id, args, kwargs)
    
def get_task_from_task_id(task_id):
    return AsyncResult(task_id, app=current_app)