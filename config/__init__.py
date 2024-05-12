"""Import the celery app when Django starts."""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from config.celery.app import app as celery_app
from config.telegram.handler import CustomTelegramHandler

__all__ = ("celery_app", "CustomTelegramHandler")
