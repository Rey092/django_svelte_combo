"""Telegram logger."""

import aiogram
import aiogram.utils.markdown as fmt
from aiogram.types import BufferedInputFile
from asgiref.sync import async_to_sync
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


class TelegramEmitter:
    """Telegram emitter."""

    def __init__(self):
        """Initialize telegram emitter."""
        self.logging_chat_id = settings.TELEGRAM_LOGGING_CHAT
        self.bot = aiogram.Bot(settings.TELEGRAM_TOKEN)

    @staticmethod
    def _prepare_text(message: str) -> str:
        """Prepare text."""
        return fmt.text(
            fmt.hbold(f"Проект: {settings.PROJECT_TITLE}."),
            fmt.hbold(f"URL: {settings.BACKEND_URL}"),
            fmt.hbold("Похоже, что что-то пошло не так!"),
            fmt.text("- - - - -"),
            fmt.hcode(f"{message}"),
            sep="\n",
        )

    def emit_sync(self, message: str, html_message: str | None = None) -> None:
        """Emit a message."""
        async_to_sync(self.emit)(message=message, html_message=html_message)

    async def emit(self, message: str, html_message: str | None = None) -> None:
        """Emit a message."""
        # prepare text
        text: fmt.text = self._prepare_text(message)

        # emit message
        if html_message:
            await self._emit_html_message(text=text, html_message=html_message)
        else:
            await self._emit_text_message(text=text)

        # close session
        await self.bot.session.close()

    async def _emit_text_message(self, text: fmt.text) -> None:
        """Emit text message."""
        await self.bot.send_message(
            chat_id=self.logging_chat_id,
            text=text,
            parse_mode="HTML",
        )

    @property
    def document_name(self) -> str:
        """Get document name.

        Format: PROJECTNAME_YYYY-MM-DD_HH-MM-SS.html
        """
        return (
            f'{slugify(settings.PROJECT_TITLE)}_'
            f'{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.html'
        )

    async def _emit_html_message(self, text: fmt.text, html_message: str) -> None:
        """Emit html message."""
        await self.bot.send_document(
            chat_id=self.logging_chat_id,
            caption=text,
            parse_mode="HTML",
            document=BufferedInputFile(
                file=html_message.encode(),
                filename=self.document_name,
            ),
        )
