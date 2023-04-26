import io

from django.core.files.base import ContentFile
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from summary.models import File
from summary.readers import read_file_content
from summary.open_ai import summarize_text

from ...utils import bot_string


async def file(update: Update, _: ContextTypes.DEFAULT_TYPE):
    status_message = await update.effective_message.reply_text(
        text=await bot_string(update.effective_user.id, 'downloading-file'),
    )

    _file = await File.objects.filter(
        file_id=update.effective_message.document.file_unique_id,
    ).aexists()

    if _file:
        return

    document = await update.effective_message.document.get_file()
    in_memory_file = io.BytesIO()
    await document.download_to_memory(out=in_memory_file)

    await status_message.edit_text(
        text=await bot_string(update.effective_user.id, 'extracting-text'),
    )

    content = read_file_content(
        mime_type=update.effective_message.document.mime_type,
        data=in_memory_file,
    )

    if not content:
        await status_message.delete()
        await update.effective_chat.send_message(
            text=await bot_string(update.effective_user.id, 'no-text-in-file')
        )
        return

    await status_message.edit_text(
        text=(await bot_string(update.effective_user.id, 'summarizing')).format(len(content)),
    )

    total_summary = []
    for page_index, text in enumerate(content, 1):
        summary = await summarize_text(text)
        total_summary.append(summary)
        if page_index == 1:
            await status_message.delete()

        await update.effective_user.send_message(
            text=(await bot_string(update.effective_user.id, 'page-summary')).format(
                page_index,
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
