from typing import TypedDict

from ...open_ai.request import create_chat_completion
from .stage import Stage


class In(TypedDict):
    content: str


class Out(TypedDict):
    content: str


class SummarizeText(Stage[In, Out]):

    def __init__(self, language: str):
        self.language = language

    async def summarize_text(self, text: str) -> str:
        command = {
            'ru': 'Переведи на русский и напиши краткое содержание в 40 словах:',
            'en': 'Summarize text in 40 words:'
        }[self.language]

        response = await create_chat_completion(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': f'{command}\n\n{text}'},
            ],
        )

        try:
            return response['choices'][0]['message']['content']
        except (IndexError, KeyError):
            return ''

    async def __call__(self, data: In) -> Out:
        result = ''
        if data['content']:
            result = await self.summarize_text(data['content'])

        return {
            'content': result,
        }
