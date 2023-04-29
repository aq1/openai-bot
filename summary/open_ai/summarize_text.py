import logging

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_KEY

logger = logging.getLogger('axiom')


async def summarize_text(language: str, text: str) -> str:
    command = {
        'ru': 'Ты обобщаешь текст в 40 словах. Ты отвечаешь только на русском',
        'en': 'You summarize text in 40 words.'
    }[language]

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f'{command}\n\n{text}'},
            ],
        )
    except openai.OpenAIError as e:
        logger.error('openai error %s', ' '.join(e.args))
        return ''

    logger.info('openai response', response)
    try:
        return response['choices'][0]['message']['content']
    except (IndexError, KeyError):
        return ''
