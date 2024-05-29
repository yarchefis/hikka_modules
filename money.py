# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site https://yarchefis.ru
# ( o.o )  🔓 Not licensed.
#  > ^ <  
# ---------------------------------------------------------------------------------
# Name: Money
# Description: Модуль для автоматического ответа "нет" на просьбы о деньгах.
# Author: yarchefis
# ---------------------------------------------------------------------------------

import logging
from telethon.tl.types import Message
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class MoneyRequestHandlerMod(loader.Module):
    """Модуль для автоматического ответа "нет" на просьбы о деньгах."""

    strings = {
        "name": "Money",
        "no_money_response": "иди нахуй блять",
    }

    keywords = [
        "дай деняг", "дай денег", "дай долг", "займи", "занять", "одолжи", "одолжить", "нужны деньги",
        "мне денег", "можешь занять", "могу занять", "денег в долг", "денег взаймы", "занять денег", "бабки", "бабло", "моней", "money"
    ]

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()  # Получаем информацию о себе

    async def watcher(self, message: Message):
        if message.is_private and message.sender_id != self.me.id:  # Проверяем, что сообщение не от самого себя
            if any(keyword in message.raw_text.lower() for keyword in self.keywords):
                await message.reply(self.strings["no_money_response"])

            # Отправляем подтверждение о прочтении
            await message.client.send_read_acknowledge(
                message.chat_id, clear_mentions=True
            )
