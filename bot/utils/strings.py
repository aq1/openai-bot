from django.conf import settings

from ..models import BotText, User


async def bot_string(user_id: int, label: str) -> str:
    text = await BotText.objects.filter(label=label).values().afirst()
    if not text:
        return ''
    user = await User.objects.filter(id=user_id).afirst()
    if not user:
        return text[settings.DEFAULT_LANGUAGE]

    return text[user.language]
