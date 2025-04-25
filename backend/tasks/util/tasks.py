import os

from django.utils import timezone
from django.core.files import File

from celery import Task
from celery import current_app
from celery.result import AsyncResult

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
        f = open(path, 'rb')
        return File(f, name=data_filename)
    
    def on_success(self, retval, task_id, args, kwargs):
        result = retval.get('result', {})
        data_filepath = retval.get('data_file', None)
        data_file = self._file_field_from_path(data_filepath) if data_filepath else None
        
        user_task_defaults = {
            'status': UserTask.TaskStatus.SUCCESS,
            'concluded_at': timezone.now(),
            'result': result,
            'data_file': data_file
        }
                
        # Atualiza o registro do UserTask com status SUCCESS e o resultado retornado
        UserTask.objects.update_or_create(
            task_id=task_id,
            defaults=user_task_defaults
        )
        
        if data_file:
            data_file.close()
        
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Atualiza o registro do UserTask com status FAILURE e o erro ocorrido
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
    
def get_task_from_task_id(task_id):
    return AsyncResult(task_id, app=current_app)