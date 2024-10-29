# Settings for Celery integration and configuration, including message brokers and tasks.

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

# Start in web
# app = Celery('settings', backend='rpc://', broker='amqp://guest:guest@rabbit:5672')

# Start in local
app = Celery("settings")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
