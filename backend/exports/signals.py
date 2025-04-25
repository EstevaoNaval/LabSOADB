import pathlib

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from import_export_extensions.models import ExportJob

from tasks.models import UserTask
from tasks.util.tasks import get_task_from_task_id

def map_export_job_status_to_user_task_status(export_job_status: ExportJob.ExportStatus):
    status_map = {
        ExportJob.ExportStatus.CREATED:      UserTask.TaskStatus.STARTED,
        ExportJob.ExportStatus.EXPORTING:    UserTask.TaskStatus.PENDING,
        ExportJob.ExportStatus.EXPORTED:     UserTask.TaskStatus.SUCCESS,
        ExportJob.ExportStatus.EXPORT_ERROR: UserTask.TaskStatus.FAILURE,
        ExportJob.ExportStatus.CANCELLED:    UserTask.TaskStatus.REVOKED,
    }
    
    return status_map.get(export_job_status, UserTask.TaskStatus.PENDING)

@receiver(post_save, sender=ExportJob)
def sync_usertask_with_exportjob(sender, instance: ExportJob, created, **kwargs):
    if not instance.export_task_id:
        return
    
    changed = False
    
    mapped_status = map_export_job_status_to_user_task_status(instance.export_status)
    file_format = pathlib.Path(instance.file_format_path).suffix.lstrip(".")
    
    ut, created_ut = UserTask.objects.get_or_create(
        task_id=instance.export_task_id,
        defaults={
            'user':       instance.created_by,
            'label':      f"Export: {file_format}",
            'status':     mapped_status,
            'created_at': timezone.now(),
            'export_job': instance,
        }
    )
    
    if created_ut:
        return
    
    # 3. Se já existia, atualiza status
    if ut.status != mapped_status:
        ut.status = mapped_status
        changed = True

    if instance.export_status in [ExportJob.ExportStatus.EXPORTED, ExportJob.ExportStatus.EXPORT_ERROR]:
        ut.concluded_at = timezone.now()

    # 4. Se terminou com sucesso, preenche result e data_file e concluded_at
    if instance.export_status == ExportJob.ExportStatus.EXPORTED:
        # JSON com referência ao arquivo
        ut.result = {
            'file': instance.data_file.name, 
            'format': file_format
        }
        
        # Copia referência do FileField
        ut.data_file = instance.data_file
        changed = True

    # 5. Em erro, só marca conclusão se ainda não tiver
    if instance.export_status == ExportJob.ExportStatus.EXPORT_ERROR:
        ut.concluded_at = timezone.now()
        ut.error_message = instance.error_message
        ut.traceback = instance.traceback
        changed = True

    if changed:
        # atualiza somente campos que mudaram
        ut.save(update_fields=['status', 'result', 'data_file', 'concluded_at', 'export_job', 'error_message', 'traceback'])