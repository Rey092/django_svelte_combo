"""Celery tasks schedule."""
from celery.schedules import crontab


class CeleryScheduleConfig:
    """Celery tasks schedule."""

    # Periodic tasks
    CELERY_BEAT_SCHEDULE = {
        "test_hello_world": {
            "task": "src.adminlte.tasks.hello_world",
            "schedule": crontab(minute="*/1"),
        },
    }
