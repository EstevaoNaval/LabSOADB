import os

from django.utils import timezone
from django.core.files import File

from celery import Task

from tasks.models import UserTask


class BaseTask(Task):
    abstract = True
    
    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = ()
        return super(BaseTask, self).__call__(*args, **kwargs)
    
    def _file_field_from_path(self, path):
        data_filename = os.path.basename(path)
            
        with open(path) as f:
            return File(f, name=data_filename)
    
    def on_success(self, retval, task_id, args, kwargs):
        result = retval.get('result', {})
        data_filepath = retval.get('data_file', None)
        
        user_task_defaults = {
            'status': UserTask.TaskStatus.SUCCESS,
            'concluded_at': timezone.now(),
            'result': result,
            'data_file': self._file_field_from_path(data_filepath) if data_filepath else None
        }
                
        # Atualiza o registro do UserTask com status SUCCESS e o resultado retornado
        UserTask.objects.update_or_create(
            task_id=task_id,
            defaults=user_task_defaults
        )
        
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Atualiza o registro do UserTask com status FAILURE e o erro ocorrido
        UserTask.objects.update_or_create(
            task_id=task_id, 
            defaults={
                'status': UserTask.TaskStatus.FAILURE,
                'result': { 'error': str(exc) },
                'concluded_at': timezone.now()
            }
        )
        
        return super().on_failure(exc, task_id, args, kwargs, einfo)