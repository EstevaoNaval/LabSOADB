from celery.contrib.abortable import AbortableTask
from celery import Task
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


class ChainedTask(AbortableTask):
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
        if len(args) == 1 and isinstance(args, dict):
            kwargs.update(args)
            args = ()
        return super(ChainedTask, self).__call__(*args, **kwargs)
    
    def check_revocation(self):
        """
        Check if task was revoked either via:
        1. Celery's internal abortion flag (is_aborted())
        2. UserTask model is_revoked flag
        
        Returns:
            bool: True if task should abort, False otherwise
        
        Usage:
            if self.check_revocation():
                # Cleanup and return
                return {'revoked': True}
        """
        # Check Celery's internal abortion flag
        if self.is_aborted():
            logger.warning(
                f'Task {self.request.id} aborted via Celery signal'
            )
            return True
        
        # Check your UserTask model for explicit revocation
        try:
            UserTask = apps.get_model('tasks', 'UserTask')
            task = UserTask.objects.filter(task_id=self.request.id).first()
            
            if task and task.is_revoked:
                logger.warning(
                    f'Task {self.request.id} revoked via UserTask model'
                )
                return True
        except Exception as e:
            logger.error(f'Error checking UserTask revocation: {e}')
        
        return False
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Called when task fails with exception.
        Triggers cleanup for resource-intensive tasks.
        """
        logger.error(f'Task {task_id} failed: {exc}')
        self._perform_cleanup(task_id, kwargs, status='FAILED')
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        Called after task execution (success, failure, revocation).
        Use this to detect revocation after task completes.
        """
        try:
            UserTask = apps.get_model('tasks', 'UserTask')
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


class BaseTask(Task):
    """
    Standard task base class (non-abortable).
    Use for tasks that don't need revocation support.
    """
    abstract = True
