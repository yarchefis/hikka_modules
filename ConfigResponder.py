# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site https://yarchefis.ru
# ( o.o )  🔓 Not licensed.
#  > ^ <  
# ---------------------------------------------------------------------------------
# Name: ConfigResponder
# Description: Отвечает на сообщения с словом "конфиг" в личных сообщениях
# Author: yarchefis
# ---------------------------------------------------------------------------------

import logging
from .. import loader  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class ConfigResponderMod(loader.Module):
    """Отвечает на сообщения с словом 'конфиг' в личных сообщениях"""

    strings = {"name": "ConfigResponder"}

    async def watcher(self, message):
        if message.is_private and "конфиг" in message.raw_text.lower():
            await message.reply("Держи!")
