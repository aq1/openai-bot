import io
from typing import TypedDict, Awaitable

from .stage import Stage
from .download_telegram_file import Out as TgOut


In = TgOut


class Out(TypedDict):
    content: str


class SaveFile(Stage[In, Out]):
    async def __call__(self, data: In) -> Out:
        return {
            'content': data['title'],
        }
