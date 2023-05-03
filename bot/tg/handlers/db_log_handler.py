import telegram
from telegram.ext import MessageHandler, filters

from ...models import Chat, TelegramUser, Message, Update


async def db_log(update: telegram.Update, _):
    await Update.objects.acreate(
        id=update.update_id,
        data=update.to_dict(),
    )

    chat, _ = await Chat.objects.aupdate_or_create(
        id=update.effective_chat.id,
        defaults=dict(
            title=update.effective_chat.title or '',
            type=update.effective_chat.type,
            username=update.effective_chat.username or '',
            data=update.effective_chat.to_dict(),
        ),
    )

    user, _ = await TelegramUser.objects.aupdate_or_create(
        id=update.effective_user.id,
        defaults=dict(
            is_bot=bool(update.effective_user.is_bot),
            is_premium=bool(update.effective_user.is_premium),
            username=update.effective_user.username or '',
            first_name=update.effective_user.first_name or '',
            last_name=update.effective_user.last_name or '',
            data=update.effective_user.to_dict(),
        ),
    )

    await Message.objects.aupdate_or_create(
        chat=chat,
        user=user,
        message_id=update.effective_message.id,
        defaults=dict(
            text=update.effective_message.text or '',
            data=update.effective_message.to_dict(),
        ),
    )


handler = MessageHandler(filters.ALL, db_log)
