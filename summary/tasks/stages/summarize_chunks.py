import asyncio
from typing import TypedDict

from .stage import Stage


class In(TypedDict):
    content: list[str]


class Out(TypedDict):
    content: list[str]


class SummarizeChunks(Stage[In, Out]):

    def __init__(self, summarize_stage: Stage):
        self.stage = summarize_stage

    async def __call__(self, data: In) -> Out:
        result = await asyncio.gather(*[
            self.stage({
                'content': content,
            })
            for content in data['content']
        ])

        return {
            'content': [r['content'] for r in result]
        }
