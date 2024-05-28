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
        if message.is_reply:
            # Если команда используется в ответ на сообщение, используем текст этого сообщения
            reply_message = await message.get_reply_message()
            text_to_echo = reply_message.raw_text
        else:
            # Получаем предыдущее сообщение в чате
            chat = await message.get_chat()
            async for msg in self.client.iter_messages(chat.id, limit=2):
                if msg.id != message.id:
                    text_to_echo = msg.raw_text
                    break
            else:
                text_to_echo = None

        if text_to_echo:
            # Оборачиваем текст в кавычки и редактируем сообщение
            await message.edit(f"\"{text_to_echo}\"")
        else:
            await message.edit(self.strings["no_previous_message"])