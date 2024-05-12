"""Users app config."""

import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Users app config."""

    name = "src.users"
    verbose_name = _("Users")

    def ready(self):
        """Import signals module."""
        with contextlib.suppress(ImportError):
            import src.users.signals  # noqa: F401
