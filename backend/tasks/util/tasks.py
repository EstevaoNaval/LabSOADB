
from celery import Task
from tasks.models import UserTask
from datetime import datetime

class BaseTask(Task):
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        # Atualiza o registro do UserTask com status SUCCESS e o resultado retornado
        UserTask.objects.filter(task_id=task_id).update(
            status='SUCCESS',
            result=retval,
            concluded_at=datetime.now()
        )
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Atualiza o registro do UserTask com status FAILURE e o erro ocorrido
        UserTask.objects.filter(task_id=task_id).update(
            status='FAILURE',
            result={'error': str(exc)},
            concluded_at=datetime.now()
        )
        return super().on_failure(exc, task_id, args, kwargs, einfo)