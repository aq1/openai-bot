from django.conf import settings
from django.utils.translation import (
    activate,
)
from telegram import Update
from telegram.ext import CallbackQueryHandler

from ...models import TelegramUser
from .l10n_context import L10nContext
from .start_handler import start_summary


async def set_language(update: Update, context: L10nContext):
    lang = context.match.group(1)
    if lang not in settings.BOT_LANGUAGES:
        return

    await TelegramUser.objects.filter(
        id=update.effective_user.id,
    ).aupdate(
        language=lang,
    )

    activate(lang)
    await update.effective_message.delete()
    await start_summary(update, context)


handler = CallbackQueryHandler(callback=set_language, pattern=r'set_lang_(\w+)')
