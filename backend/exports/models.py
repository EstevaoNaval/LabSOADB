from django.utils import timezone

from import_export_extensions.models import ExportJob as BaseExportJob

from tasks.models import UserTask

class ExportJob(BaseExportJob):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        creating = self._state.adding
        super().save(force_insert, force_update, using, update_fields)
        
        # Mapear status do ExportJob para o UserTask
        status_map = {
            'CREATED': 'STARTED',
            'EXPORTING': 'PENDING',
            'EXPORT_ERROR': 'FAILURE',
            'EXPORTED': 'SUCCESS',
            'CANCELLED': 'REVOKED'
        }

        # Criar ou atualizar o UserTask
        ut, created_ut = UserTask.objects.get_or_create(
            task_id=self.task_id,
            defaults={
                'user':      self.created_by,
                'task_name': self.task_name,
                'label':     f"Exportação de {self.resource_name}",
                'status':    status_map.get(self.status, 'PENDING'),
                'created_at': timezone.now(),
            }
        )
        # Atualiza status e resultado quando mudarem
        new_status = status_map.get(self.status, ut.status)
        if ut.status != new_status or (self.status == 'EXPORTED' and ut.result is None):
            ut.status = new_status
            # Quando concluído com sucesso, preenche o arquivo de resultado
            if self.status == 'EXPORTED' and hasattr(self, 'data_file'):
                ut.result = {'file': self.data_file.name}
                ut.concluded_at = timezone.now()
            # Em erro, também marca conclusão
            if self.status == 'EXPORT_ERROR':
                ut.concluded_at = timezone.now()
            ut.save(update_fields=['status', 'result', 'concluded_at'])

        