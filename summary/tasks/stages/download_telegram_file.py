import io
import os.path
from typing import TypedDict, BinaryIO

import telegram
from django.core.files.base import ContentFile

from ...models import File

from .stage import Stage


class In(TypedDict):
    file_id: str
    telegram_file_id: str


class Out(TypedDict):
    title: str
    content: BinaryIO


class DownloadTelegramFile(Stage[In, Out]):
    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id

    async def __call__(self, data: In) -> Out:
        _file: File | None = await File.objects.filter(
            telegram_file_id=data['telegram_file_id'],
        ).exclude(
            content='',
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

        _bytes.seek(0)
        await File.objects.aupdate_or_create(
            id=data['file_id'],
            defaults=dict(
                title=title,
                user_id=self.user_id,
                telegram_file_id=data['telegram_file_id'],
                content=ContentFile(
                    content=_bytes.read(),
                    name=title,
                ),
            ),
        )

        _bytes.seek(0)
        return {
            'title': title,
            'content': _bytes,
        }
