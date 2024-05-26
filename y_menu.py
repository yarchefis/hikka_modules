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
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class yMenuMod(loader.Module):
    """Модуль личный помощник."""

    strings = {
        "name": "yMenu",
        "config_response": "Привет, держи конфиг",
        "file_chat_id": -1002244812198,  # ID чата
        "file_message_id": 3  # ID сообщения
    }

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message: Message):
        if message.is_private:
            if any(word in message.raw_text.lower() for word in ["конфиг", "кфг", "варп", "config", "warp", "kfg"]):
                await message.reply(self.strings["config_response"])
                # Пересылаем сообщение
                await self.client(ForwardMessagesRequest(
                    from_peer=self.strings["file_chat_id"],
                    id=[self.strings["file_message_id"]],
                    to_peer=message.chat_id,
                    with_my_score=False
                ))
