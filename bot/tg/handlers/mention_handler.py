from telegram import Update, MessageEntity
from telegram.ext import MessageHandler, filters

from .message_handler import call_summarize_text_task
from .l10n_context import L10nContext


async def mention(update: Update, context: L10nContext):
    if update.effective_message.text != f'@{context.bot.username}':
        return

    message = update.effective_message.reply_to_message
    text = message.text or message.caption

    await call_summarize_text_task(
        text,
        update,
        context,
    )


handler = MessageHandler(filters=filters.ChatType.GROUPS & filters.Entity(MessageEntity.MENTION), callback=mention)
