import logging

import telegram
from telegram.ext import MessageHandler, filters


logger = logging.getLogger('axiom')


async def log(update: telegram.Update, _):
    logger.info('bot update', update.to_dict())


handler = MessageHandler(filters.ALL, log)
