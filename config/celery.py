# -*- coding: utf-8 -*-
"""
Celery App.
"""

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

app_celery = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app_celery.config_from_object("django.conf:settings", namespace="CELERY")
app_celery.conf.broker_connection_retry_on_startup = False

# Load task modules from all registered Django app configs.
app_celery.autodiscover_tasks()
