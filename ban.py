import logging
from telethon import events
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class AutoBlockerMod(loader.Module):
    """Модуль для автоматического блокирования пользователей."""

    strings = {
        "name": "AutoBlocker",
        "block_message": "Извини, но меня поставили сюда следить за сообщениями. По правилам мне придется тебя заблокировать, это хозяин не хочет принимать PM сообщения."
    }

    def __init__(self):
        # Здесь добавлены ID пользователей, которых нельзя блокировать
        self.whitelist = {
            831408739,
            8027906376,
            1628112862,
            5731587578,
            5142620829,
            1113636161,
            6939483738,
            5381998466,
            1512882126,
            1988845082,
            1336120316,
            5234377340,
            1515756886,
            388246260,
            6593286426,
            1219923771
        }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.watcher(incoming=True)
    async def watcher(self, message):
        if message.is_private and message.sender_id != self.client.me.id:
            if message.sender_id not in self.whitelist:
                # Отправляем сообщение пользователю
                await message.reply(self.strings["block_message"])
                
                # Блокируем пользователя
                await self.client.block_user(message.sender_id)
                
                # Удаляем переписку с пользователем
                await self.client.delete_messages(message.peer_id, message.id)

                # Отправляем сообщение в группу о блокировке
                group_id = -1004578705952  # ID вашей группы
                block_notification = f"Был заблокирован @{message.sender.username}.\nЕго сообщение: {message.raw_text}"
                await self.client.send_message(group_id, block_notification)
