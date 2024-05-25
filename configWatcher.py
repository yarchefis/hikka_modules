# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site htts;//yarchefis.ru
# ( o.o )  🔓 Not licensed.
#  > ^ <  
# ---------------------------------------------------------------------------------
# Name: ConfigWatcher
# Description: Автоматически отвечает "Держи!" на сообщения, содержащие слово "конфиг".
# Author: yarchefis
# ---------------------------------------------------------------------------------

from .. import loader

@loader.tds
class ConfigWatcherMod(loader.Module):
    """Автоматически отвечает "Держи!" на сообщения, содержащие слово "конфиг"."""

    strings = {"name": "ConfigWatcher"}

    async def watcher(self, message):
        if message.mentioned and "конфиг" in message.raw_text.lower():
            await message.client.send_message(message.chat_id, "Держи!", reply_to=message.id)
