import telegram

from .stage import Stage


class TelegramNotification(Stage):
    def __init__(self, token: str, chat_id: int, message_id: int):
        self.bot = telegram.Bot(token)
        self.chat_id = chat_id
        self.message_id = message_id
        self.notification_message_id: int = 0

    def __call__(self, text: str):
        async def notify_and_pass_data(data: any):
            if self.notification_message_id:
                await self.bot.edit_message_text(
                    text=text,
                    chat_id=self.chat_id,
                    message_id=self.notification_message_id,
                )
            else:
                self.notification_message_id = (await self.bot.send_message(
                    text=text,
                    chat_id=self.chat_id,
                    reply_to_message_id=self.message_id,
                )).id

            return data

        return notify_and_pass_data
