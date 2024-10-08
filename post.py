import random
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDiscussionMessageRequest
from telethon.tl.types import InputPeerChannel
from .. import loader, utils

@loader.tds
class CommentNewPostsMod(loader.Module):
    """Модуль для комментирования новых постов в канале"""

    strings = {"name": "CommentNewPosts"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.target_channel_username = 'yarchefis_channel'  # Юзернейм целевого канала

        # Получаем информацию о канале
        self.channel_entity = await client.get_entity(self.target_channel_username)
        self.channel_id = self.channel_entity.id

        # Массив фраз для комментариев
        self.comments = [
    "Давайте общаться без грубостей и оскорблений 🙏",
    "Уважайте друг друга, без мата и ругани 🌿",
    "Без ненормативной лексики, пожалуйста 😇",
    "Не забываем про вежливость в общении! 💬✨",
    "Будьте добры в общении, без агрессии 🌸",
    "Мирные разговоры без грубых слов 🕊️",
    "Я ПЕРВЫЙ! И да, мат тут неуместен ❌🗣️",
    "Давайте сохранять спокойствие и вежливость 🙌",
    "Ваши слова важны — не используйте оскорбления 🗣️❗",
    "Помните: хорошее общение — без грубости 💫",
    "Я ПЕРВЫЙ! И да, давайте уважать друг друга и не ругаться 🤝",
    "Будем соблюдать правила — без ругани и мата 📝🫶",
    "Пожалуйста, выражайтесь корректно и уважительно 💡",
    "Я ПЕРВЫЙ! И да, без грубых слов наше общение будет лучше 🌟",
    "Общение без оскорблений — залог хорошей беседы 🌿"
]

    @loader.watcher(incoming=True, chats='yarchefis_channel')
    async def watcher(self, message):
        # Проверяем, что сообщение новое и является постом в канале
        if message.is_channel and message.to_id.channel_id == self.channel_id and not message.out:
            try:
                # Получаем обсуждение поста (комментарии)
                discussion = await self.client(GetDiscussionMessageRequest(
                    peer=InputPeerChannel(self.channel_id, self.channel_entity.access_hash),
                    msg_id=message.id
                ))

                # Выбираем случайную фразу
                comment = random.choice(self.comments)

                # Отправляем комментарий к посту
                await self.client.send_message(
                    entity=discussion.messages[0].to_id,
                    message=comment,
                    reply_to=discussion.messages[0].id
                )
            except Exception as e:
                self.log.error(f"Failed to comment on post: {e}")