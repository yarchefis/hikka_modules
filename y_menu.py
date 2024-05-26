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
                await self.client.send_file(message.chat_id, self.strings["file_url"])

