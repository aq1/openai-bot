import asyncio
from dataclasses import dataclass
from typing import Callable, Type

from django.conf import settings
from telegram.ext import Application, ContextTypes, BaseHandler, CallbackContext

from ..models import TelegramUser

from .handlers import (
    call_task_handler,
    db_log_handler,
    feedback_handler,
    file_handler,
    log_handler,
    mention_handler,
    message_handler,
    set_language_handler,
    start_handler,
    generate_dalle_handler,
    create_dalle_variation_handler,
)

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


@dataclass
class Bot:
    name: str
    token: str
    post_init: Callable[[Application], any]
    post_stop: Callable[[Application], any]
    context_type: Type[CallbackContext]
    handlers: list[list[str]]

    def start(self):
        application = Application.builder().token(
            self.token,
        ).post_init(
            self.post_init,
        ).post_stop(
            self.post_stop
        ).context_types(
            ContextTypes(context=self.context_type),
        ).concurrent_updates(
            True,
        ).build()

        for group_id, handlers in enumerate(self.handlers):
            application.add_handlers(handlers, group=group_id)

        application.run_polling()


BOTS = [
    Bot(
        name='summary',
        token=settings.SUMMARY_TELEGRAM_TOKEN,
        post_init=notify('Summary initialized'),
        post_stop=notify('Summary stopped'),
        context_type=L10nContext,
        handlers=[
            [
                start_handler.summary_start_handler,
                file_handler.handler,
                set_language_handler.handler,
                call_task_handler.handler,
                feedback_handler.handler,
                mention_handler.handler,
                message_handler.handler,
            ],
            [
                db_log_handler.handler,
            ],
            [
                log_handler.handler,
            ],
        ],
    ),
    Bot(
        name='dalle',
        token=settings.DALLE_TELEGRAM_TOKEN,
        post_init=notify('Dall-e initialized'),
        post_stop=notify('Dall-e stopped'),
        context_type=L10nContext,
        handlers=[
            [
                start_handler.dalle_start_handler,
                generate_dalle_handler.handler,
                create_dalle_variation_handler.handler,
            ],
            [
                db_log_handler.handler,
            ],
            [
                log_handler.handler,
            ], ],
    ),
]
