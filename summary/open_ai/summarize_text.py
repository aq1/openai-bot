import logging

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_KEY

logger = logging.getLogger('axiom')


async def summarize_text(language: str, text: str) -> str:
    command = {
        'ru': 'О чём текст?',
        'en': 'Summarize text'
    }[language]

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{command}:\n{text}"},
            ]
        )
    except openai.OpenAIError:
        logger.exception('openai error')
        return ''

    logger.info('openai response', response)
    try:
        return response['choices'][0]['message']['content']
    except (IndexError, KeyError):
        return ''
