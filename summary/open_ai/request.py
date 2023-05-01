import logging

import openai
from django.conf import settings

from ..models import OpenAICall

logger = logging.getLogger('axiom')

openai.api_key = settings.OPENAI_KEY


def log_to_db(func):
    async def _f(*args, **kwargs):
        response = await func(*args, **kwargs)
        await OpenAICall.objects.acreate(
            request={
                'args': args,
                'kwargs': kwargs,
            },
            response=response,
            tokens=response.get('usage', {}).get('total_tokens', 0),
        )
        return response

    return _f


@log_to_db
async def create_chat_completion(model: str, messages: list[dict[str, str]]):
    try:
        return await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
        )
    except openai.OpenAIError as e:
        logger.error('openai error %s', ' '.join(e.args))
        return ''
