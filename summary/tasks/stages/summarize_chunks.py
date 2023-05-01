from typing import TypedDict

from .stage import Stage
from .summarize_text import SummarizeText


class In(TypedDict):
    content: list[str]


class Out(TypedDict):
    content: list[str]


class SummarizeChunks(Stage[In, Out]):

    def __init__(self, language: str):
        self.stage = SummarizeText(language=language)

    async def __call__(self, data: In) -> Out:
        result = []
        for content in data['content']:
            result.append((await self.stage({
                'content': content,
            }))['content'])

        return {
            'content': result
        }
