"""Celery App."""

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

import configurations  # noqa: E402

configurations.setup()

# Create and configure the app.
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = False

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
