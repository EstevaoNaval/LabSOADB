import os
import logging
from celery import Celery
from kombu import Queue, Exchange

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsoa_website_backend.settings')

app = Celery('labsoa_website_backend')

pdf2chemicals_tasks_dlx = Exchange(
    'pdf2chemicals_tasks_dlx', 
    type='direct'
)
pdf2chemicals_tasks_dlq = Queue(
    'pdf2chemicals_tasks_dlq',
    pdf2chemicals_tasks_dlx,
    routing_key='dlq_pdf2chemicals'
)

app.conf.task_queues = (
    Queue(
        'django_tasks', 
        routing_key='light.#', 
        max_priority=10
    ),  # Alta prioridade
    Queue(
        'pdf2chemicals_tasks',
        exchange=Exchange('main', type='direct'), 
        routing_key='heavy.#', 
        max_priority=5,
        queue_arguments={
            'x-dead-letter-exchange': 'pdf2chemicals_tasks_dlx',
            'x-dead-letter-routing-key': 'pdf2chemicals_tasks_dlq',
            'x-max-length': 10000 # Queue size limit
        }
    ),  # Baixa prioridade
)

app.conf.task_default_queue = 'django_tasks'  # Padrão para tasks leves
app.conf.task_routes = {
    'chemicals.tasks.light_task_*': {'queue': 'django_tasks'},
    'pdf2chemicals_service.tasks.heavy_task_*': {'queue': 'pdf2chemicals_tasks'},
}

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

# Configurar o logging para Celery
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('celery')

@app.task(bind=True)
def debug_task(self):
    logger.info(f'Request: {self.request!r}')