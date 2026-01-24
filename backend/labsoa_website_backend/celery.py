import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsoa_website_backend.settings')

app = Celery('labsoa_website_backend')

# ============================================
# QUEUE DEFINITIONS (only thing in celery.py)
# ============================================

django_tasks = Queue(
    'django_tasks',
    exchange=Exchange('django_tasks', type='direct', durable=True),
    routing_key='light.#',
    durable=True,
    max_priority=10
)

# Dead letter exchange
pdf2chemicals_dlx = Exchange(
    'pdf2chemicals_tasks_dlx',
    type='direct',
    durable=True
)

# Dead letter queue
pdf2chemicals_dlq = Queue(
    'pdf2chemicals_tasks_dlq',
    pdf2chemicals_dlx,
    routing_key='dlq_pdf2chemicals',
    durable=True,
    queue_arguments={
        'x-message-ttl': 7 * 24 * 60 * 60 * 1000,
        'x-max-length': 100000,
    },
)

# Main queue
pdf2chemicals_tasks = Queue(
    'pdf2chemicals_tasks',
    exchange=Exchange('pdf2chemicals_tasks', type='direct', durable=True),
    routing_key='heavy.#',
    durable=True,
    max_priority=5,
    queue_arguments={
        'x-dead-letter-exchange': 'pdf2chemicals_tasks_dlx',
        'x-dead-letter-routing-key': 'dlq_pdf2chemicals',
        'x-message-ttl': 7 * 60 * 60 * 1000,
        'x-max-length': 50000,
    },
)

# Register queues
app.conf.task_queues = (django_tasks, pdf2chemicals_tasks)
app.conf.task_default_queue = 'django_tasks'

# Task routing
app.conf.task_routes = {
    'pdf2chemicals_service.tasks.*': {'queue': 'pdf2chemicals_tasks'},
    'chemicals.tasks.*': {'queue': 'django_tasks'},
}

# ============================================
# LOAD SETTINGS (Everything else from Django)
# ============================================

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()