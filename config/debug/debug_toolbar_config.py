"""Debug toolbar configuration."""


class DebugToolbarConfig:
    """Debug toolbar configuration."""

    # django-debug-toolbar: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    THIRD_PARTY_APPS = ["debug_toolbar"]

    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    # ips: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
