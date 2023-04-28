from typing import BinaryIO

import PyPDF2


def read(content: BinaryIO) -> str:
    pdf_reader = PyPDF2.PdfReader(content)
    return '\n'.join([
        p.extract_text() for p in pdf_reader.pages
    ])
