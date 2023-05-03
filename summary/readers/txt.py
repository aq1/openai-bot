from typing import BinaryIO


def read(content: BinaryIO) -> str:
    return str(content.read())
