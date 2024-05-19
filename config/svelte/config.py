"""Svelte configuration class."""

from pathlib import Path

from configurations import values
from inertia.utils import InertiaJsonEncoder

# TODO: from ninja.responses import NinjaJSONEncoder


# noinspection PyPep8Naming
class InertiaConfig:
    """Svelte configuration class."""

    # variables
    DEBUG: bool
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # installed apps
    INERTIA_INSTALLED_APPS = [
        "inertia",
        "django_vite",
    ]

    # middleware
    INERTIA_MIDDLEWARE = [
        "config.svelte.middleware.InertiaMiddleware",
    ]

    # dirs
    INERTIA_STATICFILES_DIRS = [
        BASE_DIR / "dist",
    ]

    # Django Vite server port for local development.
    DJANGO_VITE_DEV_SERVER_PORT = values.IntegerValue(3000, environ_prefix=None)

    # Inertia: https://github.com/inertiajs/inertia-django
    INERTIA_LAYOUT = "svelte.html"
    INERTIA_SSR_ENABLED = False
    INERTIA_VERSION = "1.0.0"
    INERTIA_JSON_ENCODER = InertiaJsonEncoder

    @property
    def DJANGO_VITE_DEV_MODE(self):  # noqa: N802
        """Returns vite working mode.

        If True, renders link to local ViteJS HMR (Hot Module Replacement)
        server. to update the frontend in real-time.
        If False, renders link to the production ViteJS build assets.
        """
        return self.DEBUG

    @property
    def DJANGO_VITE_MANIFEST_PATH(self):  # noqa: N802
        """Path to the ViteJS manifest file.

        This file contains the mapping between the original and the hashed file names.
        """
        return self.BASE_DIR / "staticfiles" / "manifest.json"
