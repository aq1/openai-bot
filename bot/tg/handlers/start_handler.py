from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler

from django.utils.translation import gettext as _

from .l10n_context import L10nContext


async def start(update: Update, __: L10nContext):
    await update.effective_chat.send_message(
        text=_(
            'With this bot, you can easily extract short summaries from PDF, TXT and DOCX files in seconds. '
            'Simply upload the file you want to extract a summary from, '
            'and our bot will take care of the rest.\n\n'
            'It can also summarize messages you send or forward.\n\n'
            'In group chats reply to message and mention bot to summarize that message.\n\n'
            'Type /feedback for bugs/questions/feedback.'
        ),
        reply_markup=InlineKeyboardMarkup.from_row([
            InlineKeyboardButton(
                text='🇺🇸',
                callback_data='set_lang_en',
            ),
            InlineKeyboardButton(
                text='🇷🇺',
                callback_data='set_lang_ru',
            ),
        ]),
    )


handler = CommandHandler('start', start)
