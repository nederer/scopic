from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scopic_task.settings')

app = Celery('scopic_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
