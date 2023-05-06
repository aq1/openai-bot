import openai
from typing import TypedDict

from django.utils.translation import gettext as _

from .exceptions import StopPipeline
from ...open_ai.request import create_chat_completion
from .stage import Stage


class In(TypedDict):
    content: str


class Out(TypedDict):
    content: str


class SummarizeText(Stage[In, Out]):

    def __init__(self, user_id: int, language: str):
        self.user_id = user_id
        self.language = language

    async def summarize_text(self, text: str) -> str:
        command = {
            'ru': 'Переведи на русский и напиши краткое содержание в 40 словах:',
            'en': 'Summarize text in 40 words:'
        }[self.language]

        try:
            response = (await create_chat_completion(
                user_id=self.user_id,
                model='gpt-4',
                messages=[
                    {'role': 'user', 'content': f'{command}\n\n{text}'},
                ],
            ))['choices'][0]['message']['content']
        except (IndexError, KeyError, openai.OpenAIError):
            raise StopPipeline(_('😥 Sorry, could not process your request'))

        return response

    async def __call__(self, data: In) -> Out:
        result = ''
        if data['content']:
            result = await self.summarize_text(data['content'])

        return {
            'content': result,
        }
