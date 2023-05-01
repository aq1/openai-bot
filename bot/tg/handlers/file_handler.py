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
        id=file_unique_id,
    ).afirst()


def split_content_by_tokens_length(content: str) -> tuple[int, list[str]]:
    encoding = tiktoken.get_encoding('cl100k_base')
    tokens = encoding.encode(content)
    content_chunks = []
    for i in range(0, len(tokens), settings.MAX_TOKENS_PER_PART):
        content_chunks.append(encoding.decode(tokens[i:i + settings.MAX_TOKENS_PER_PART]))

    return len(tokens), content_chunks


async def summarize_content_chunks(language: str, content_chunks: list[str]):
    for part_index, text in enumerate(content_chunks, 1):
        if not text:
            continue
        yield await summarize_text(
            language=language,
            text=text,
        )


async def save_file(
        document_bytes: BinaryIO,
        file_unique_id: str,
        file_id: str,
        user_id: int,
        title: str,
        tokens: int,
):
    document_bytes.seek(0)
    await File.objects.aupdate_or_create(
        id=file_unique_id,
        defaults=dict(
            telegram_file_id=file_id,
            user_id=user_id,
            title=title,
            tokens=tokens,
            content=ContentFile(
                name=title,
                content=document_bytes.read(),
            ),
        ),
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


def format_status(status: list[list[str]]) -> str:
    return '\n'.join(' '.join(s) for s in status)


async def file(update: Update, context: L10nContext):

    from summary.tasks.summarize_file import summarize_file

    d = update.effective_message.document
    content = await summarize_file(
        file_id=d.file_unique_id,
        telegram_file_id=d.file_id,
        language='ru',
        chat_id=1,
        message_id=1,
    )

    await update.effective_message.reply_text(
        text=content,
    )

    return

    _file = await check_file(update.effective_message.document.file_unique_id)

    status = [
        ['☑️', await context.s('downloading-file')],
        ['◽️', await context.s('extracting-text')],
        ['◽️', await context.s('summarizing')],
    ]

    status_message = await update.effective_chat.send_message(
        text=format_status(status),
        reply_to_message_id=update.effective_message.id,
    )

    if _file:
        document_bytes = _file.content
    else:
        document_bytes = await download_file(update.effective_message.document)

    status[0] = ['✅️', await context.s('downloading-file-done')]
    status[1][0] = '☑️'
    await status_message.edit_text(
        text=format_status(status),
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

    tokens_count, content_chunks = split_content_by_tokens_length(content)

    status[1] = [
        '✅️',
        (await context.s('extracting-text-done')).format(
            parts_count_to_str(context.user.language, len(content_chunks))
        )
    ]
    status[2][0] = '☑️'
    await status_message.edit_text(
        text=format_status(status),
    )

    total_summary = []
    part = 0
    status_text = status[2][1]
    async for summary in summarize_content_chunks(context.user.language, content_chunks):
        part += 1
        if not summary:
            continue
        total_summary.append(summary)

        if part < len(content_chunks):
            status[2][1] = f'{status_text} {part}/{len(content_chunks)}'
            await status_message.edit_text(
                text=format_status(status),
            )

    summary = total_summary[0]
    if len(total_summary) > 1:
        summary = await summarize_text(context.user.language, '\n'.join(total_summary))

    await update.effective_chat.send_message(
        text=summary,
    )

    status[2] = ['✅️', await context.s('summarizing-done')]
    await status_message.edit_text(
        text=format_status(status),
    )
    await save_file(
        file_id=update.effective_message.document.file_id,
        file_unique_id=update.effective_message.document.file_unique_id,
        user_id=update.effective_user.id,
        title=update.effective_message.document.file_name,
        document_bytes=document_bytes,
        tokens=tokens_count,
    )


handler = MessageHandler(filters=filters.Document.ALL, callback=file)
