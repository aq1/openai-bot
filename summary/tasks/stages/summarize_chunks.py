import asyncio
from typing import TypedDict

from .stage import Stage
from .summarize_text import SummarizeText


class In(TypedDict):
    content: list[str]


class Out(TypedDict):
    content: list[str]


class SummarizeChunks(Stage[In, Out]):

    def __init__(self, summarize_stage: Stage):
        self.stage = summarize_stage

    async def __call__(self, data: In) -> Out:
        result = []
        async with asyncio.TaskGroup() as tg:
            for content in data['content']:
                task = tg.create_task(self.stage({
                    'content': content,
                }))
                result.append(task)

        return {
            'content': [t.result()['content'] for t in result]
        }
