from django.conf import settings
from telegram.ext import Application

from .handlers import HANDLER_GROUPS


def start_bot():
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    for group_id, handlers in enumerate(HANDLER_GROUPS):
        for handler in handlers:
            application.add_handler(handler, group=group_id)

    application.run_polling()
