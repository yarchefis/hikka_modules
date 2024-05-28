import logging
from telethon import events
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class EchoMod(loader.Module):
    """Модуль для редактирования сообщения на предыдущее сообщение в чате."""

    strings = {
        "name": "EchoMod",
        "no_previous_message": "⚠️ Нет предыдущего сообщения, которое можно было бы использовать."
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    @loader.ratelimit
    async def echocmd(self, message):
        """Редактировать сообщение на предыдущее сообщение в чате."""
        chat = await message.get_chat()
        # Получаем список сообщений, включая текущее сообщение
        async for msg in self.client.iter_messages(chat.id, limit=2):
            if msg.id != message.id:
                previous_message = msg
                break
        else:
            previous_message = None

        if previous_message:
            await message.edit(previous_message.raw_text)
        else:
            await message.edit(self.strings["no_previous_message"])