from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, filters

from django.utils.translation import gettext as _

from .l10n_context import L10nContext

from summary.tasks import generate_image


async def generate_dalle(update: Update, context: L10nContext):
    if not update.effective_message.text:
        return

    result = await generate_image(
        bot_token=context.bot.token,
        user_id=update.effective_user.id,
        prompt=update.effective_message.text,
        chat_id=update.effective_message.chat_id,
        message_id=update.effective_message.id,
    )

    if not result['url']:
        return

    await update.effective_message.reply_photo(
        photo=result['url'],
        caption=result['db_image'].prompt,
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=_('Try another variation'),
                callback_data=f'create_variation_{result["db_image"].id}',
            ),
        ),
    )


handler = MessageHandler(filters=filters.ChatType.PRIVATE & filters.TEXT, callback=generate_dalle)
