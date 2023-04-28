from django.conf import settings
from telegram.ext import Application, ContextTypes

from .handlers import HANDLER_GROUPS
from .handlers.l10n_context import L10nContext


def start_bot():
    context_types = ContextTypes(context=L10nContext)
    application = Application.builder().token(settings.TELEGRAM_TOKEN).context_types(context_types).build()
    for group_id, handlers in enumerate(HANDLER_GROUPS):
        for handler in handlers:
            application.add_handler(handler, group=group_id)

    application.run_polling()
