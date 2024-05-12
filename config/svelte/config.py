"""Svelte configuration class."""

from pathlib import Path

from configurations import values
from ninja.responses import NinjaJSONEncoder


# noinspection PyPep8Naming
class SvelteConfig:
    """Svelte configuration class."""

    # variables
    DEBUG: bool
    BASE_DIR: Path

    # installed apps
    SVELTE_INSTALLED_APPS = [
        "inertia",
        "django_vite",
    ]

    # middleware
    SVELTE_MIDDLEWARE = [
        "base.inertia.middleware.InertiaMiddleware",
    ]

    # Django Vite server port for local development.
    DJANGO_VITE_DEV_SERVER_PORT = values.IntegerValue(3000, environ_prefix=None)

    # Inertia: https://github.com/inertiajs/inertia-django
    INERTIA_LAYOUT = "svelte.html"
    INERTIA_SSR_ENABLED = False
    INERTIA_VERSION = "1.0.0"
    INERTIA_JSON_ENCODER = NinjaJSONEncoder

    @property
    def SVELTE_STATICFILES_DIRS(self):  # noqa: N802
        """Path to the ViteJS build assets."""
        return [self.BASE_DIR / "dist"]

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
