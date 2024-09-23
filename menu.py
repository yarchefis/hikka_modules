from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class MenuMod(loader.Module):
    """Модуль для отображения меню с кнопками"""

    strings = {
        "name": "Menu",
        "menu_message": "📝 <b>Выберите опцию:</b>",
    }

    async def client_ready(self, client, db):
        self._me = await client.get_me()

    @loader.command
    async def menu(self, message: Message):
        """Показать меню"""
        if message.from_id != self._me.id:
            await message.reply("У вас нет прав на использование этой команды.")
            return

        buttons = [
            [{"text": "Опция 1", "callback": self._handle_option1}],
            [{"text": "Опция 2", "callback": self._handle_option2}],
            # Добавьте другие кнопки по мере необходимости
        ]

        await message.reply(
            self.strings("menu_message"),
            reply_markup={"inline_keyboard": buttons},
        )

    async def _handle_option1(self, call):
        await call.answer("Вы выбрали опцию 1!")

    async def _handle_option2(self, call):
        await call.answer("Вы выбрали опцию 2!")
