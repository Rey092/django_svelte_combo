"""Debug toolbar configuration."""


class RequestsTrackerConfig:
    """Debug toolbar configuration."""

    # requests-tracker: https://pypi.org/project/requests-tracker/#install-the-package
    THIRD_PARTY_APPS = ["requests_tracker"]

    # requests-tracker: https://pypi.org/project/requests-tracker/#install-the-package
    MIDDLEWARE = [
        "requests_tracker.middleware.requests_tracker_middleware",
    ]

    # ips: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

    # config: currently only for ignoring debug toolbar requests
    REQUESTS_TRACKER_CONFIG = {
        "IGNORE_PATHS_PATTERNS": (
            # regex pattern to check if string contains '__debug__'
            ".*/__debug__/*",
        ),
    }
