import io
import os.path
from typing import TypedDict, BinaryIO

import telegram

from ...models import File

from .stage import Stage


class In(TypedDict):
    telegram_file_id: str


class Out(TypedDict):
    title: str
    content: BinaryIO


class DownloadTelegramFile(Stage[In, Out]):
    def __init__(self, token: str):
        self.token = token

    async def __call__(self, data: In) -> Out:
        _file: File | None = await File.objects.filter(
            telegram_file_id=data['telegram_file_id'],
        ).afirst()

        if _file:
            return {
                'title': _file.title,
                'content': _file.content.file,
            }

        document = await telegram.Bot(self.token).get_file(
            file_id=data['telegram_file_id'],
        )

        _bytes = io.BytesIO()
        await document.download_to_memory(out=_bytes)

        try:
            title = os.path.split(document.file_path)[-1]
        except IndexError:
            title = str(document.file_path) or 'untitled'

        return {
            'title': title,
            'content': _bytes,
        }
