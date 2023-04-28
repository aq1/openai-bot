import io
from typing import BinaryIO

from django.conf import settings
from django.core.files.base import ContentFile
from telegram import Update, Document
from telegram.ext import MessageHandler, filters
import tiktoken

from summary.models import File
from summary.readers import read_file_content
from summary.open_ai import summarize_text

from .l10n_context import L10nContext


async def download_file(document: Document) -> BinaryIO:
    document = await document.get_file()
    _bytes = io.BytesIO()
    await document.download_to_memory(out=_bytes)
    return _bytes


async def check_file(file_unique_id) -> File | None:
    return await File.objects.filter(
        file_id=file_unique_id,
    ).afirst()


def split_content_by_tokens_length(content: str) -> list[str]:
    encoding = tiktoken.get_encoding('cl100k_base')
    tokens = encoding.encode(content)
    content_chunks = []
    for i in range(0, len(tokens), settings.MAX_TOKENS_PER_TEXT):
        content_chunks.append(encoding.decode(tokens[i:i + settings.MAX_TOKENS_PER_TEXT]))

    return content_chunks


async def summarize_content_chunks(language: str, content_chunks: list[str]):
    for part_index, text in enumerate(content_chunks, 1):
        if not text:
            continue
        yield await summarize_text(
            language=language,
            text=text,
        )


async def save_file(document_bytes: BinaryIO, file_id: str, user_id: int, title: str, summary: list[str]):
    document_bytes.seek(0)
    await File.objects.acreate(
        file_id=file_id,
        user_id=user_id,
        title=title,
        content=ContentFile(
            name=title,
            content=document_bytes.read(),
        ),
        summary=summary,
    )


def parts_count_to_str(language: str, count: int) -> str:
    if language == 'en':
        if count == 1:
            return '1 part'
        return f'{count} parts'
    if language == 'ru':
        c = abs(count) % 100
        n1 = c % 10
        w = 'частей'
        if 10 < c < 20:
            w = 'часть'

        if 1 < n1 < 5:
            w = 'части'

        if n1 == 1:
            w = 'часть'

        return f'{count} {w}'

    return f'{count}'


async def file(update: Update, context: L10nContext):
    _file = await check_file(update.effective_message.document.file_unique_id)
    if _file and _file.summary:
        await update.effective_chat.send_message(
            text='\n\n'.join(_file.summary),
        )
        return

    status_message = await update.effective_chat.send_message(
        text=await context.s('downloading-file'),
        reply_to_message_id=update.effective_message.id,
    )

    document_bytes = await download_file(update.effective_message.document)

    await status_message.edit_text(
        text=await context.s('extracting-text'),
    )

    content = read_file_content(
        mime_type=update.effective_message.document.mime_type,
        data=document_bytes,
    )

    if not content:
        await status_message.delete()
        await update.effective_chat.send_message(
            text=await context.s('no-text-in-file')
        )
        return

    content_chunks = split_content_by_tokens_length(content)

    await status_message.edit_text(
        text=(await context.s('summarizing')).format(parts_count_to_str(context.user.language, len(content_chunks))),
    )

    total_summary = []
    async for summary in summarize_content_chunks(context.user.language, content_chunks):
        if not summary:
            continue
        total_summary.append(summary)
        await update.effective_chat.send_message(
            text=summary,
        )

    await status_message.delete()

    await save_file(
        file_id=update.effective_message.document.file_unique_id,
        user_id=update.effective_user.id,
        title=update.effective_message.document.file_name,
        document_bytes=document_bytes,
        summary=total_summary,
    )


handler = MessageHandler(filters=filters.Document.ALL, callback=file)
