import os

from celery import Celery
from kombu import Queue

from src.core.enums import CeleryQueue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.task_queues = (
    Queue(name=CeleryQueue.MANAGE_QUEUE),
    Queue(name=CeleryQueue.BROWSER_SCRAPING_QUEUE),
    Queue(name=CeleryQueue.REQUEST_SCRAPING_QUEUE)
)
