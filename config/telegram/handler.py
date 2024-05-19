"""Custom Telegram Handler."""

import contextlib
from logging import LogRecord
from typing import Any

from django.conf import settings
from django_telegram_logging.handler import TelegramHandler

from config.telegram.emitter import TelegramEmitter


class CustomTelegramHandler(TelegramHandler):
    """Custom Telegram Handler."""

    def send_message(self, message, html_message):
        """Send a message to telegram."""
        emitter: TelegramEmitter = TelegramEmitter()
        emitter.emit_sync(message, html_message)

    @staticmethod
    def get_exc_info_and_message(record: LogRecord) -> tuple:
        """Get exc_info and message from the record."""
        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        exc_type = exc_info[0].__name__ if exc_info[0] else "Exception"
        message = f"{exc_type}({exc_info[1]})"
        return exc_info, message

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_request(record: LogRecord):
        """Get request from the record."""
        try:
            request = record.request
        except AttributeError:
            request = None
        return request

    @staticmethod
    def append_request_path_to_message(message, request):
        """Append request path to the message."""
        with contextlib.suppress(AttributeError):
            message += f' at "{request.path}"'
        return message

    def get_reporter_and_html_message(self, request, exc_info):
        """Get reporter and html message."""
        reporter = self.reporter_class(request, *exc_info)
        try:
            html_message = reporter.get_traceback_html()
        except AttributeError:
            html_message = ""
        return reporter, html_message

    def emit(self, record: LogRecord) -> None:
        """Emit a record."""
        # run checks
        if not settings.TELEGRAM_LOGGING_ENABLED:
            return

        print(settings.TELEGRAM_LOGGING_ENABLED)  # noqa: T201

        # process record
        request = self.get_request(record)
        exc_info, message = self.get_exc_info_and_message(record)
        message = self.append_request_path_to_message(message, request)

        # TODO: remove after a fix in the django-telegram-logging package
        should_send_message: bool = self.check_if_should_send_message(exc_info)

        # check if a message should be sent
        if not should_send_message:
            return

        # get reporter and html message
        _, html_message = self.get_reporter_and_html_message(request, exc_info)

        # send message
        # self.send_message(message, html_message)  # noqa: ERA001

    @staticmethod
    def check_if_should_send_message(exc_info: Any) -> bool:
        """Check if a message should be sent to the telegram.

        TODO: Wait for a fix in the django-telegram-logging package.
         https://github.com/eadwinCode/django-ninja-extra/releases
         Need to wait next release after 0.20.7 to delete this method.
        """
        # try to get status code from the exception message
        status_code: int | None = None
        try:
            status: str = str(exc_info[1])
            status_code: int = int(status.split(" ")[-1])
        except ValueError:
            pass

        # if status code exists and lover than 500, don't send a message
        if status_code and status_code < 500:  # noqa: PLR2004
            return False

        return True
