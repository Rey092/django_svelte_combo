"""Telegram configuration settings."""

from configurations import values


# noinspection PyPep8Naming
class CeleryConfig:
    """Telegram configuration settings."""

    # Types
    TIME_ZONE: str
    REDIS_URL: str

    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
    CELERY_RESULT_BACKEND = "django-db"
    CELERY_RESULT_EXTENDED = True
    CELERY_CACHE_BACKEND = "default"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
    # https://github.com/celery/celery/pull/6122
    CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
    CELERY_RESULT_BACKEND_MAX_RETRIES = 10
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
    CELERY_ACCEPT_CONTENT = ["json"]
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
    CELERY_TASK_SERIALIZER = "json"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
    CELERY_RESULT_SERIALIZER = "json"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
    # TODO: set to whatever value is adequate in your circumstances
    CELERY_TASK_TIME_LIMIT = 5 * 60
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
    # TODO: set to whatever value is adequate in your circumstances
    CELERY_TASK_SOFT_TIME_LIMIT = 60
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
    CELERY_WORKER_SEND_TASK_EVENTS = True
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
    CELERY_TASK_SEND_SENT_EVENT = True

    @property
    def CELERY_TIMEZONE(self):  # noqa: N802
        """Celery timezone."""
        return self.TIME_ZONE

    @property
    def CELERY_BROKER_URL(self):  # noqa: N802
        """Get Celery broker URL.

        https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
        """
        return values.Value(
            self.REDIS_URL, environ_prefix=None, environ_name="CELERY_BROKER_URL"
        )


class CeleryLocalConfig(CeleryConfig):
    """Celery configuration settings for local development."""

    # Eager https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-always-eager
    CELERY_TASK_ALWAYS_EAGER = values.BooleanValue(default=True, environ_prefix=None)
    # Celery propagation: https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
    CELERY_TASK_EAGER_PROPAGATES = True
