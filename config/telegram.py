"""Telegram configuration settings."""

from configurations import values


class TelegramConfig:
    """Telegram configuration settings."""

    TELEGRAM_TOKEN = TELEGRAM_LOGGING_TOKEN = values.Value(
        default=None,
        environ_name="TELEGRAM_LOGGING_TOKEN",
        environ_prefix=None,
    )
    TELEGRAM_LOGGING_CHAT = values.Value(
        default=None,
        environ_name="TELEGRAM_LOGGING_CHAT",
        environ_prefix=None,
    )
    TELEGRAM_LOGGING_EMIT_ON_DEBUG = values.Value(
        default=False,
        environ_name="TELEGRAM_LOGGING_EMIT_ON_DEBUG",
        environ_prefix=None,
    )
