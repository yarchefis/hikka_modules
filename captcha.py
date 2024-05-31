# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: CaptchaModerator
# Author: OpenAI
# Description: Mutes new users in a specific chat until they confirm a captcha.
# Commands:
#   None
# ---------------------------------------------------------------------------------

from telethon import events, Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from .. import loader, utils

class CaptchaModeratorMod(loader.Module):
    """Mutes new users in a specific chat until they confirm a captcha"""

    strings = {"name": "CaptchaModerator"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.tds
    async def watcher(self, message):
        chat_id = -1002030594496  # Replace with the target chat ID

        if message.chat_id != chat_id:
            return

        if message.user_joined or message.user_added:
            user_id = message.action_message.from_id if message.user_joined else message.action_message.added_by
            mute_rights = ChatBannedRights(until_date=None, send_messages=True)
            await self.client(EditBannedRequest(chat_id, user_id, mute_rights))

            button = [Button.inline("Подтверди капчу", b"captcha_confirm")]
            await self.client.send_message(chat_id, "Подтверди капчу", buttons=button, reply_to=message.id)

    @loader.callback_handler()
    async def captcha_callback(self, event):
        if event.data != b"captcha_confirm":
            return

        user_id = event.sender_id
        chat_id = event.chat_id
        unmute_rights = ChatBannedRights(until_date=None, send_messages=False)
        await self.client(EditBannedRequest(chat_id, user_id, unmute_rights))
        await event.edit("Капча подтверждена. Вы размучены.")
