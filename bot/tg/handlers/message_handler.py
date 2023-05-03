from telegram import Update
from telegram.ext import MessageHandler, filters

from summary.tasks import summarize_text

from .l10n_context import L10nContext


async def message(update: Update, context: L10nContext):
    text = update.effective_message.text or update.effective_message.caption

    if not text:
        return

    result = await summarize_text(
        user_id=update.effective_user.id,
        text=text,
        language=context.language,
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.id,
    )

    if not result['content']:
        return

    await update.effective_message.reply_text(
        text=result['content'],
    )


handler = MessageHandler(filters=filters.TEXT | filters.FORWARDED, callback=message)
