import os
from typing import TypedDict, BinaryIO, Callable

from django.utils.translation import gettext as _

from .stage import (
    Stage,
)

from .exceptions import (
    StopPipeline,
)

from ...readers import (
    pdf,
    docx,
    txt,
)


class In(TypedDict):
    title: str
    content: BinaryIO


class Out(TypedDict):
    content: str


readers: dict[str, Callable[[BinaryIO], str]] = {
    '.pdf': pdf.read,
    '.docx': docx.read,
    '.txt': txt.read,
}


class ReadFile(Stage[In, Out]):
    async def __call__(self, data: In) -> Out:
        reader = readers.get(os.path.splitext(data['title'])[1])
        if not reader:
            raise StopPipeline(_('This file format is not supported.'))

        return {
            'content': reader(data['content']).strip()
        }
