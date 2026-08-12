import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stock.settings')

# The variable name here is "app"
app = Celery('Stock')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# Stock/celery.py — add after app.autodiscover_tasks()
print("CELERY BROKER:", app.conf.broker_url)
print("CELERY RESULT BACKEND:", app.conf.result_backend)