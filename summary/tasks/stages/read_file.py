import os
from typing import TypedDict, BinaryIO, Callable

from .stage import (
    Stage,
    StopPipeline,
)

from ...readers import (
    pdf,
    docx,
)


class In(TypedDict):
    title: str
    content: BinaryIO


class Out(TypedDict):
    content: str


readers: dict[str, Callable[[BinaryIO], str]] = {
    '.pdf': pdf.read,
    '.docx': docx.read,
}


class ReadFile(Stage[In, Out]):
    async def __call__(self, data: In) -> Out:
        reader = readers.get(os.path.splitext(data['title'])[1])
        if not reader:
            raise StopPipeline('invalid_file_format')

        return {
            'content': reader(data['content']).strip()
        }
