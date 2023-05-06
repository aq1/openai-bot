from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

from django.utils.translation import gettext as _

from .l10n_context import L10nContext

from summary.tasks import create_image_variation


async def create_dalle_variation(update: Update, context: L10nContext):
    await update.callback_query.answer()

    try:
        file_id = int(context.match.group(1))
    except (ValueError, AttributeError):
        return

    result = await create_image_variation(
        bot_token=context.bot.token,
        user_id=update.effective_user.id,
        file_id=file_id,
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


handler = CallbackQueryHandler(pattern=r'create_variation_(\d+)', callback=create_dalle_variation)
