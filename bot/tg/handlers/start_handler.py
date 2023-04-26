from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from ...utils import bot_string


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        text=await bot_string(update.effective_user.id, 'start'),
    )


handler = CommandHandler('start', start)
