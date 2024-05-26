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
from telethon.tl.functions.messages import GetMessagesRequest
from telethon.tl.types import InputMessageID
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class yMenuMod(loader.Module):
    """Модуль личный помощник."""

    strings = {
        "name": "yMenu",
        "config_response": "Привет, держи конфиг",
        "file_url": "https://t.me/c/2244812198/3"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message: Message):
        if message.is_private:
            if any(word in message.raw_text.lower() for word in ["конфиг", "кфг", "варп", "config", "warp", "kfg"]):
                await message.reply(self.strings["config_response"])
                
                # Получаем сообщение с файлом
                file_message = await self.client(GetMessagesRequest(
                    peer=await self.client.get_input_entity('t.me/c/2244812198'),
                    id=[InputMessageID(id=3)]
                ))

                if file_message and file_message.messages:
                    file = file_message.messages[0].media
                    if file:
                        await self.client.send_file(message.chat_id, file)

