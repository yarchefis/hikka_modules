import asyncio
from telethon import events, types, utils
from telethon.tl.functions.messages import CreateForumTopicRequest
from telethon.tl.types import ChatAdminRights

from .. import loader, utils

class ChatArchiveMod(loader.Module):
    """Archive personal messages to group chat topics"""

    strings = {
        "name": "ChatArchive",
        "group_not_found": "❗️ Group chat for archiving not found.",
        "archive_enabled": "✅ Archiving enabled.",
        "archive_disabled": "❌ Archiving disabled.",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "ARCHIVE_GROUP_NAME", "Chat Archive", "Name of the group to create topics for PMs"
        )
        self._archive_enabled = False
        self._archive_group_id = None
        self._topics = {}

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self._me = await client.get_me()
        await self._check_or_create_group()

    async def _check_or_create_group(self):
        async for dialog in self._client.iter_dialogs():
            if dialog.name == self.config["ARCHIVE_GROUP_NAME"] and isinstance(dialog.entity, types.Chat):
                self._archive_group_id = dialog.id
                return

        # If the group doesn't exist, notify the user
        await self._client.send_message(
            self._me.id, self.strings("group_not_found")
        )

    async def _create_topic(self, user):
        topic_title = utils.escape_html(utils.get_display_name(user))
        topic = await self._client(CreateForumTopicRequest(
            channel=self._archive_group_id,
            title=topic_title,
            icon_color=0x42b1f5  # Blue color, change as needed
        ))
        return topic.topic.id

    async def _get_or_create_topic(self, user_id, user):
        if user_id in self._topics:
            return self._topics[user_id]
        
        topic_id = await self._create_topic(user)
        self._topics[user_id] = topic_id
        return topic_id

    async def _archive_message(self, message):
        if not self._archive_enabled or not message.is_private:
            return

        user = await message.get_sender()
        topic_id = await self._get_or_create_topic(message.sender_id, user)
        await self._client.forward_messages(self._archive_group_id, message, topic_id=topic_id)

    async def _forward_last_messages(self, user_id):
        messages = await self._client.get_messages(user_id, limit=100)
        for message in reversed(messages):
            await self._archive_message(message)

    async def watcher(self, message):
        if not self._archive_enabled:
            return
        await self._archive_message(message)

    async def archivecmd(self, message):
        """Enable or disable archiving"""
        self._archive_enabled = not self._archive_enabled
        if self._archive_enabled:
            await message.edit(self.strings("archive_enabled"))
            async for dialog in self._client.iter_dialogs():
                if dialog.is_user and not dialog.entity.bot:
                    await self._forward_last_messages(dialog.id)
        else:
            await message.edit(self.strings("archive_disabled"))

# Add this module to the __main__.py or your bot's main script.