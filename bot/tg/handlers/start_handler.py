from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler

from .l10n_context import L10nContext


async def start(update: Update, context: L10nContext):
    await update.effective_chat.send_message(
        text=await context.s('start'),
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
