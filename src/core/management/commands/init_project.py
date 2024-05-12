"""Module for the management command 'init_project'."""

import logging

from django.conf import settings
from django.core.management import BaseCommand

from src.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for basic data initialization."""

    def handle(
        self,
        *args,
        **options,
    ):
        """Handle command."""
        logger.info("Creating basic data")
        self._create_superuser()
        logger.info("Basic data created")

    @classmethod
    def _create_superuser(cls):
        """Create test superuser."""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
            )
            logger.info("Superuser created")
        else:
            logger.info("Superuser already exists, updating password and email")
            superuser = User.objects.get(is_superuser=True)
            superuser.email = settings.SUPERUSER_EMAIL
            superuser.set_password(settings.SUPERUSER_PASSWORD)
            superuser.save()
            logger.info("Superuser updated")
