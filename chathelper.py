import re
from telethon import events
from .. import loader, utils

class LinkModeratorMod(loader.Module):
    """Deletes messages with links in a specific chat and mutes the user for 1 day"""

    strings = {"name": "LinkModerator"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.tds
    async def watcher(self, message):
        chat_id = -1002030594496  # Replace with the target chat ID
        link_pattern = re.compile(r'https?://|http?://')

        if message.chat_id == chat_id and link_pattern.search(message.raw_text):
            await message.delete()
            await self.client.send_message(message.chat_id, ".mute 1d надо читать правила")
