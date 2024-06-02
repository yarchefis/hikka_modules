from telethon import events
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights
import time

from .. import loader, utils

@loader.tds
class MuteOnJoinMod(loader.Module):
    """Заглушает пользователей, которые присоединяются к чату"""

    strings = {
        "name": "MuteOnJoin",
        "mute_msg": "🤫 Добро пожаловать! Вы были заглушены на 1 минуту..",
        "mute_in_chat": "✅ Заглушение при входе включено в этом чате.",
        "unmute_in_chat": "🚫 Заглушение при входе выключено в этом чате.",
        "no_perms": "🤷‍♂️ У меня нет прав для заглушения пользователей в этом чате.",
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        muted_chats = db.get("muteonjoin_chats")
        self._muted_chats = set(muted_chats) if muted_chats else set()

    async def on_unload(self):
        self._db.set("muteonjoin_chats", list(self._muted_chats))

    @loader.command(ru_doc="Включить заглушение в этом чате")
    async def mutein(self, message: events.NewMessage.Event):
        """Включить заглушение в этом чате"""
        chat = await message.get_chat()

        if not chat.admin_rights or not chat.admin_rights.ban_users:
            await utils.answer(message, self.strings("no_perms"))
            return

        try:
            await self._client(
                EditChatDefaultBannedRightsRequest(
                    chat.id,
                    ChatBannedRights(
                        until_date=2**31 - 1,
                        send_messages=True,
                    ),
                )
            )
        except Exception:
            await utils.answer(message, self.strings("no_perms"))
            return

        self._muted_chats.add(chat.id)
        await utils.answer(message, self.strings("mute_in_chat"))

    @loader.command(ru_doc="Отключить заглушение в этом чате")
    async def muteout(self, message: events.NewMessage.Event):
        """Отключить заглушение в этом чате"""
        chat = await message.get_chat()

        self._muted_chats.discard(chat.id)
        await utils.answer(message, self.strings("unmute_in_chat"))

    @loader.loop(interval=1, autostart=True)
    async def watcher(self):
        for chat_id in self._muted_chats:
            # Подписываемся на события join/add в этом чате
            @events.register(
                events.NewMessage(chats=[chat_id], incoming=True),
                disable_errors=True,
            )
            async def mute_on_join(event: events.NewMessage.Event):
                if (
                    event.message.action
                    and (
                        event.message.action.user_joined
                        or event.message.action.user_added
                    )
                ):
                    # Заглушаем пользователя на 1 минуту
                    user_id = (
                        event.message.action.user_joined.user_id
                        if event.message.action.user_joined
                        else event.message.action.user_added.user_id
                    )
                    await self._client(
                        EditChatDefaultBannedRightsRequest(
                            chat_id,
                            ChatBannedRights(
                                until_date=time.time() + self.config["mute_duration"],
                                send_messages=True,
                            ),
                            user_id,
                        )
                    )
                    # Отправляем сообщение о заглушении
                    await event.respond(self.strings("mute_msg"))
                    return

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "mute_duration", 60, "Длительность заглушения в секундах"
            )
        )
