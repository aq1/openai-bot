from typing import BinaryIO

from . import (
    pdf,
    docx,
)

readers = {
    'application/pdf': pdf.read,
}


def read_file_content(mime_type: str, data: BinaryIO) -> str:
    reader = readers.get(mime_type)
    if not reader:
        return ''

    return reader(data).strip()
