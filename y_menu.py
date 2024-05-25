# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site https://yarchefis.ru
# ( o.o )  🔓 Not licensed.
#  > ^ <  
# ---------------------------------------------------------------------------------
# Name: MenuButton
# Description: Модуль, который отправляет сообщение с кнопкой по команде .menu и отвечает на личные сообщения с клавиатурой
# Author: yarchefis
# Commands:
# .menu
# ---------------------------------------------------------------------------------

import logging
from telethon.tl.types import Message
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class MenuButtonMod(loader.Module):
    """Модуль, который отправляет сообщение с кнопкой по команде .menu и отвечает на личные сообщения с клавиатурой"""

    strings = {
        "name": "MenuButton",
        "menu_message": "Нажмите на кнопку ниже:",
        "choose_action": "Выберите действие:",
        "hold_message": "Держи!",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def menucmd(self, message: Message):
        """Отправить сообщение с кнопкой"""
        await self.inline.form(
            message=message,
            text=self.strings["menu_message"],
            reply_markup=[
                [{"text": "Нажми меня", "callback": self.inline__button_pressed}]
            ],
        )

    async def inline__button_pressed(self, call):
        await call.answer("Привет!", show_alert=True)

    async def watcher(self, message: Message):
        if message.is_private:
            await self.inline.form(
                message=message,
                text=self.strings["choose_action"],
                reply_markup=[
                    [{"text": "Конфиг warp", "callback": self.send_hold_message}]
                ],
            )

    async def send_hold_message(self, call):
        await call.answer(self.strings["hold_message"], show_alert=True)
