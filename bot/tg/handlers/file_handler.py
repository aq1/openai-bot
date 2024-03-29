from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, filters

from django.utils.translation import gettext as _

from summary.tasks import summarize_file
from summary.models import File

from .l10n_context import L10nContext


async def file(update: Update, context: L10nContext):
    d = update.effective_message.document

    await File.objects.aupdate_or_create(
        id=d.file_unique_id,
        defaults=dict(
            user_id=update.effective_user.id,
            telegram_file_id=d.file_id,
            title=d.file_name,
        ),
    )

    result = await summarize_file(
        bot_token=context.bot.token,
        user_id=update.effective_user.id,
        file_id=d.file_unique_id,
        telegram_file_id=d.file_id,
        language=context.language,
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.id,
    )

    if not result['content']:
        return

    await update.effective_message.reply_text(
        text=result['content'],
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=_('Run again'),
                callback_data=f'summarize_file_{d.file_unique_id}',
            ),
        ),
    )


handler = MessageHandler(filters=filters.Document.ALL, callback=file)
