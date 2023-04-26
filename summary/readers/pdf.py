import io

import PyPDF2


def read(content: io.BytesIO) -> list[str]:
    pdf_reader = PyPDF2.PdfReader(content)
    return [
        p.extract_text() for p in pdf_reader.pages
    ]
