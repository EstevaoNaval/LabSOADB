from django.utils import timezone

from import_export_extensions.models import ExportJob as BaseExportJob

from tasks.models import UserTask

class ExportJob(BaseExportJob):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        
        # Mapear status do ExportJob para o UserTask
        status_map = {
            self.ExportStatus.CREATED:   UserTask.TaskStatus.STARTED,
            self.ExportStatus.EXPORTING: UserTask.TaskStatus.PENDING,
            self.ExportStatus.EXPORTED:  UserTask.TaskStatus.SUCCESS,
            self.ExportStatus.EXPORT_ERROR: UserTask.TaskStatus.FAILURE,
            self.ExportStatus.CANCELLED: UserTask.TaskStatus.REVOKED,
        }
        
        mapped = status_map.get(self.export_status, UserTask.STATUS_PENDING)

        print("Cheguei até aqui.")
        
        # Criar ou atualizar o UserTask
        ut, created_ut = UserTask.objects.get_or_create(
            task_id=self.export_task_id,
            defaults={
                'user': self.created_by,
                'task_name': self.task_name,
                'label': f"Export: {self.file_format.get_extension()}",
                'status': mapped,
                'created_at': timezone.now(),
            }
        )
        
        # Atualiza status e resultado quando mudarem
        changed = False
        if ut.status != mapped:
            ut.status = mapped
            changed = True

        # Se chegou em SUCCESS (EXPORTED), popule resultado
        if self.export_status == self.ExportStatus.EXPORTED and not ut.result:
            ut.data_file = self.data_file.name
            ut.concluded_at = timezone.now()
            changed = True

        # Se erro, também marca conclusão
        if self.export_status == self.ExportStatus.EXPORT_ERROR and not ut.concluded_at:
            ut.concluded_at = timezone.now()
            changed = True

        if changed:
            ut.save(update_fields=['status', 'data_file', 'concluded_at'])

        