from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, filters

from django.utils.translation import gettext as _

from summary.models import File
from summary.tasks.summarize_file import summarize_file
from .l10n_context import L10nContext


async def call_task(update: Update, context: L10nContext):
    _file = await File.objects.filter(
        id=context.match.group(1),
    ).afirst()

    if not _file:
        return

    result = await summarize_file(
        user_id=_file.user_id,
        file_id=_file.id,
        telegram_file_id=_file.telegram_file_id,
        language='ru',
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.id,
    )

    await update.effective_message.reply_text(
        text=result['content'],
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=_('Again'),
                callback_data=f'summarize_file_{_file.id}',
            ),
        ),
    )


handler = CallbackQueryHandler(pattern='summarize_file_(.+)', callback=call_task)
