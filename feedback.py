# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site https://yarchefis.ru/
# ( o.o )  🔓 Not licensed.
#  > ^ < 
# ---------------------------------------------------------------------------------
# Name: Feedback
# Description: Модуль для отправки сообщения с ссылкой на фидбек.
# Author: yarchefis
# Commands:
# .feed
# ---------------------------------------------------------------------------------

from .. import loader, utils

@loader.tds
class FeedbackModule(loader.Module):
    """Модуль для отправки сообщения с ссылкой на фидбек."""

    strings = {"name": "Feedback"}

    @loader.command()
    async def feed(self, message):
        """Отправить сообщение с ссылкой на фидбек"""
        feedback_link = '<a href="http://t.me/hikka_xxbo0l_bot?start=feedback">ссылке</a>'
        text = f'Вы можете отправить фидбек на {feedback_link}'
        await utils.answer(message, text)
