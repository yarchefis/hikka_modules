# ---------------------------------------------------------------------------------
#  /\_/\  🌐 Этот модуль был загружен через https://t.me/hikkamods_bot
# ( o.o )  🔐 Лицензирован под GNU AGPLv3.
#  > ^ <   ⚠️ Владелец heta.hikariatama.ru не несет ответственности или интеллектуальных прав на этот скрипт
# ---------------------------------------------------------------------------------
# Name: MuteNewUsers
# Author: OpenAI
# Description: Модуль для автоматического заглушения новых пользователей в чате
# Commands:
#   mutein - подписывает/отписывает данный чат для наблюдения
# ---------------------------------------------------------------------------------

from telethon import events, Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from .. import loader, utils

class MuteNewUsersMod(loader.Module):
    """Модуль для автоматического заглушения новых пользователей в чате"""

    strings = {"name": "MuteNewUsers"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.muted_chats = self.db.get(self.strings["name"], "muted_chats", [])

    async def mute_user(self, chat_id, user_id):
        mute_rights = ChatBannedRights(until_date=None, send_messages=True)
        await self.client(EditBannedRequest(chat_id, user_id, mute_rights))
        button = [Button.inline("Подтвердите, что вы не бот", b"captcha_confirm")]
        await self.client.send_message(chat_id, "Вы были заглушены. Подтвердите, что вы не бот.", buttons=button)

    @loader.tds
    async def muteincmd(self, message):
        """Подписывает/отписывает данный чат для наблюдения"""
        chat_id = utils.get_chat_id(message)
        if chat_id in self.muted_chats:
            self.muted_chats.remove(chat_id)
            self.db.set(self.strings["name"], "muted_chats", self.muted_chats)
            await message.edit("<b>Чат удалён из списка наблюдения.</b>")
        else:
            self.muted_chats.append(chat_id)
            self.db.set(self.strings["name"], "muted_chats", self.muted_chats)
            await message.edit("<b>Чат добавлен в список наблюдения.</b>")

    @loader.tds
    async def watcher(self, message):
        if message.chat_id not in self.muted_chats:
            return

        if message.user_joined or message.user_added:
            user_id = message.action_message.from_id if message.user_joined else message.action_message.added_by
            await self.mute_user(message.chat_id, user_id)

    @loader.callback_handler()
    async def captcha_callback(self, event):
        if event.data != b"captcha_confirm":
            return

        user_id = event.sender_id
        chat_id = event.chat_id
        unmute_rights = ChatBannedRights(until_date=None, send_messages=False)
        await self.client(EditBannedRequest(chat_id, user_id, unmute_rights))
        await event.edit("Вы были размучены. Спасибо за подтверждение.")
