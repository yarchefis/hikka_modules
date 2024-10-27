import logging
from telethon import events
from .. import loader  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class SimpleResponderMod(loader.Module):
    """Модуль для автоматического ответа на сообщения."""

    strings = {
        "name": "SimpleResponder",
        "response_message": "Извини, но меня поставили сюда следить за сообщениями. По правилам я не могу продолжать разговор."
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.watcher(incoming=True)
    async def watcher(self, message):
        if message.is_private and message.sender_id != self.client.me.id:
            # Отправляем ответ пользователю
            await message.reply(self.strings["response_message"])
