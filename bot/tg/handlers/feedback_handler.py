from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from django.utils import translation
from django.utils.translation import gettext as _

from ...models import TelegramUser
from .l10n_context import L10nContext

FEEDBACK = 1


async def feedback(update: Update, __: L10nContext):
    await update.effective_message.reply_text(
        text=_('Your feedback is received. Thank you.'),
    )

    users = TelegramUser.objects.filter(
        groups__name='Feedback',
    )

    async for user in users:
        message = await update.effective_message.forward(
            chat_id=user.id,
        )
        await message.reply_text(
            text=f'{update.effective_user.username or update.effective_user.first_name}\n{update.effective_message.id}'
        )

    return ConversationHandler.END


async def start_feedback_conversation(update: Update, __: L10nContext):
    await update.effective_chat.send_message(
        text=_('Please share your feedback with us'),
        reply_markup=ReplyKeyboardMarkup.from_button(
            button=KeyboardButton(
                text=_('Cancel'),
            ),
            resize_keyboard=True,
        ),
    )
    return FEEDBACK


async def cancel_feedback(update: Update, __: L10nContext):
    await update.effective_chat.send_message(
        text='Ok',
        reply_markup=ReplyKeyboardRemove(),
    )


def gettext_in(language, s):
    with translation.override(language):
        return translation.gettext(s)


handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command='feedback',
            filters=filters.ChatType.PRIVATE,
            callback=start_feedback_conversation,
        ),
    ],
    states={
        FEEDBACK: [
            MessageHandler(
                filters=filters.ChatType.PRIVATE & filters.Text([
                    gettext_in('ru', 'Cancel'),
                    gettext_in('en', 'Cancel'),
                ]),
                callback=cancel_feedback,
            ),
            MessageHandler(
                filters=filters.ChatType.PRIVATE & filters.TEXT,
                callback=feedback,
            ),
        ]
    },
    fallbacks=[],
)
