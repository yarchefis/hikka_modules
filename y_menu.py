# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site https://yarchefis.ru
# ( o.o )  🔓 Not licensed.
#  > ^ <  
# ---------------------------------------------------------------------------------
# Name: yMenu
# Description: Модуль личный помощник.
# Author: yarchefis
# ---------------------------------------------------------------------------------

import logging
from telethon.tl.types import Message
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.users import GetFullUserRequest
from .. import loader, utils  # type: ignore
from time import time

logger = logging.getLogger(__name__)

@loader.tds
class yMenuMod(loader.Module):
    """Модуль личный помощник."""

    strings = {
        "name": "yMenu",
        "config_response": "Привет, держи конфиг",
        "file_chat_id": -1002244812198,  # ID чата
        "file_message_id": 3,  # ID сообщения
        "spam_wait_time": 60  # Время ожидания в секундах между сообщениями
    }

    def __init__(self):
        self.last_sent = {}  # Словарь для отслеживания времени последней отправки сообщения каждому пользователю

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()  # Получаем информацию о себе

    async def watcher(self, message: Message):
        if message.is_private and message.sender_id != self.me.id:  # Проверяем, что сообщение не от самого себя
            if any(word in message.raw_text.lower() for word in ["конфиг", "кфг", "варп", "config", "warp", "kfg"]):
                now = time()
                if message.sender_id not in self.last_sent or now - self.last_sent[message.sender_id] > self.strings["spam_wait_time"]:
                    self.last_sent[message.sender_id] = now
                    await message.reply(self.strings["config_response"])
                    # Пересылаем сообщение
                    await self.client(ForwardMessagesRequest(
                        from_peer=self.strings["file_chat_id"],
                        id=[self.strings["file_message_id"]],
                        to_peer=message.chat_id,
                        with_my_score=False
                    ))
                else:
                    logger.info(f"Spam protection: Ignored message from {message.sender_id}")

