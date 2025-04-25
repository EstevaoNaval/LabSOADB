from celery import shared_task

from exports.models import ExportJob

@shared_task()
def export_data_task(job_id: int):
    """Async task for starting data export."""
    job = ExportJob.objects.get(id=job_id)
    job.export_data()