import asyncio

from django.conf import settings
from telegram.ext import Application, ContextTypes

from ..models import TelegramUser

from .handlers import HANDLER_GROUPS
from .handlers.l10n_context import L10nContext


def notify(text: str):
    async def func(application: Application):
        users = TelegramUser.objects.filter(groups__name='Admin')
        async with asyncio.TaskGroup() as tg:
            async for user in users:
                tg.create_task(application.bot.send_message(
                    chat_id=user.id,
                    text=text,
                ))

    return func


def start_bot():
    context_types = ContextTypes(context=L10nContext)

    application = Application.builder().token(
        settings.TELEGRAM_TOKEN,
    ).post_init(
        notify('Initialized'),
    ).post_stop(
        notify('Stopped'),
    ).context_types(
        context_types,
    ).concurrent_updates(
        True,
    ).build()

    for group_id, handlers in enumerate(HANDLER_GROUPS):
        application.add_handlers(handlers, group=group_id)

    application.run_polling()
