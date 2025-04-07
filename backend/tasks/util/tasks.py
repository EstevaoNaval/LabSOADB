
from celery import Task
from tasks.models import UserTask
from django.utils import timezone

class BaseTask(Task):
    abstract = True
    
    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = ()
        return super(BaseTask, self).__call__(*args, **kwargs)
    
    def on_success(self, retval, task_id, args, kwargs):
        # Atualiza o registro do UserTask com status SUCCESS e o resultado retornado
        UserTask.objects.filter(task_id=task_id).update(
            status='SUCCESS',
            result=retval,
            concluded_at=timezone.now()
        )
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Atualiza o registro do UserTask com status FAILURE e o erro ocorrido
        UserTask.objects.filter(task_id=task_id).update(
            status='FAILURE',
            result={'error': str(exc)},
            concluded_at=timezone.now()
        )
        return super().on_failure(exc, task_id, args, kwargs, einfo)