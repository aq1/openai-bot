from django.conf import settings
from django.utils.translation import (
    activate,
)
from telegram import Update
from telegram.ext import CallbackQueryHandler

from ...models import User
from .l10n_context import L10nContext
from .start_handler import start


async def set_language(update: Update, context: L10nContext):
    lang = context.match.group(1)
    if lang not in settings.BOT_LANGUAGES:
        return

    await User.objects.filter(
        id=update.effective_user.id,
    ).aupdate(
        language=lang,
    )

    activate(lang)
    await update.effective_message.delete()
    await start(update, context)


handler = CallbackQueryHandler(callback=set_language, pattern=r'set_lang_(\w+)')
