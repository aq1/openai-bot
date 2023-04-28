from django.conf import settings
from telegram.ext import CallbackContext, ExtBot, Application

from ...models import User, BotText


class L10nContext(CallbackContext[ExtBot, dict, dict, dict]):
    def __init__(self, application: Application, chat_id: int = None, user_id: int = None):
        super().__init__(application=application, chat_id=chat_id, user_id=user_id)
        self.user_id: int | None = user_id
        self.user: User | None = None

    async def s(self, label: str) -> str:
        if not self.user:
            self.user = await User.objects.filter(id=self.user_id).afirst()

        text = await BotText.objects.values().aget(label=label)

        if self.user:
            return text[self.user.language]

        return text[settings.DEFAULT_LANGUAGE]
