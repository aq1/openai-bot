import io
from docx2python import docx2python


def read(content: io.BytesIO) -> str:
    with docx2python(content) as docx_content:
        return docx_content.text
