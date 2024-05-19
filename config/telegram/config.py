"""Telegram configuration settings."""

from configurations import values


class TelegramConfig:
    """Telegram configuration settings."""

    TELEGRAM_TOKEN = TELEGRAM_LOGGING_TOKEN = values.Value(
        default=None,
        environ_name="TELEGRAM_TOKEN",
        environ_prefix=None,
    )
    TELEGRAM_LOGGING_CHAT = values.Value(
        default=None,
        environ_name="TELEGRAM_LOGGING_CHAT",
        environ_prefix=None,
    )
    TELEGRAM_LOGGING_ENABLED = values.Value(
        default=False,
        environ_name="TELEGRAM_LOGGING_ENABLED",
        environ_prefix=None,
    )


class TelegramLoggingConfig(TelegramConfig):
    """Telegram logging configuration settings."""

    # Logging: https://docs.djangoproject.com/en/5.0/topics/logging/
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "telegram": {
                "level": "ERROR",
                "class": "config.telegram.handler.CustomTelegramHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "django.request": {
                "handlers": ["console", "telegram"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console", "telegram"],
                "propagate": True,
            },
        },
    }
