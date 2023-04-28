import io

from django.conf import settings
from django.core.files.base import ContentFile
from telegram import Update
from telegram.ext import MessageHandler, filters
import tiktoken

from summary.models import File
from summary.readers import read_file_content
from summary.open_ai import summarize_text

from ...models import User
from .l10n_context import L10nContext


async def file(update: Update, context: L10nContext):
    _file = await File.objects.filter(
        file_id=update.effective_message.document.file_unique_id,
    ).aexists()

    if _file:
        return

    status_message = await update.effective_chat.send_message(
        text=await context.s('downloading-file'),
        reply_to_message_id=update.effective_message.id,
    )

    document = await update.effective_message.document.get_file()
    in_memory_file = io.BytesIO()
    await document.download_to_memory(out=in_memory_file)

    await status_message.edit_text(
        text=await context.s('extracting-text'),
    )

    content = read_file_content(
        mime_type=update.effective_message.document.mime_type,
        data=in_memory_file,
    )

    if not content:
        await status_message.delete()
        await update.effective_chat.send_message(
            text=await context.s('no-text-in-file')
        )
        return

    encoding = tiktoken.get_encoding('cl100k_base')
    tokens = encoding.encode(content)
    content_chunks = []
    for i in range(0, len(tokens), settings.MAX_TOKENS_PER_TEXT):
        content_chunks.append(encoding.decode(tokens[i:i + settings.MAX_TOKENS_PER_TEXT]))

    await status_message.edit_text(
        text=(await context.s('summarizing')).format(len(content_chunks)),
    )

    total_summary = []
    for part_index, text in enumerate(content_chunks, 1):
        if not text:
            continue
        summary = await summarize_text(
            language=(await User.objects.filter(id=update.effective_user.id).afirst()).language,
            text=text,
        )
        total_summary.append(summary)
        if part_index == 1:
            await status_message.delete()

        await update.effective_user.send_message(
            text=(await context.s('page-summary')).format(
                part_index,
                summary,
            ),
        )

    in_memory_file.seek(0)
    await File.objects.acreate(
        file_id=update.effective_message.document.file_unique_id,
        user_id=update.effective_user.id,
        title=update.effective_message.document.file_name,
        content=ContentFile(
            name=update.effective_message.document.file_name,
            content=in_memory_file.read(),
        ),
        summary=total_summary,
    )


handler = MessageHandler(filters=filters.Document.ALL, callback=file)
