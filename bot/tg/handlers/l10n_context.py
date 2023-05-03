from django.conf import settings
from django.utils.translation import activate
from telegram.ext import CallbackContext, ExtBot, Application

from ...models import User


class L10nContext(CallbackContext[ExtBot, dict, dict, dict]):
    def __init__(self, application: Application, chat_id: int = None, user_id: int = None):
        super().__init__(application=application, chat_id=chat_id, user_id=user_id)
        self.user_id: int | None = user_id
        self.language: str = settings.DEFAULT_LANGUAGE

    async def refresh_data(self) -> None:
        user = await User.objects.filter(id=self.user_id).afirst()
        if user:
            self.language = user.language

        activate(self.language)
        return await super().refresh_data()
