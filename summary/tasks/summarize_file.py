from typing import TypedDict

from django.conf import settings
from django.utils.translation import gettext as _

from .stages.exceptions import (
    StopPipeline,
)

from .stages import (
    Pipeline,
    SummarizeChunks,
    IfStage,
    Idle,
    DownloadTelegramFile,
    ReadFile,
    SummarizeText,
    SplitByTokensLength,
    JoinText,
    TelegramNotification,
    CheckQuota,
)


class In(TypedDict):
    telegram_file_id: str


class Out(TypedDict):
    content: str


async def summarize_file(
        user_id: int,
        file_id: str,
        telegram_file_id: str,
        language: str,
        chat_id: int,
        message_id: int,
) -> Out:
    notify = TelegramNotification(
        token=settings.TELEGRAM_TOKEN,
        chat_id=chat_id,
        message_id=message_id,
    )

    summarize_text = SummarizeText(
        language=language,
        user_id=user_id,
    )

    summarize_pipeline: Pipeline[In, Out] = Pipeline(
        stages=[
            CheckQuota(
                user_id=user_id,
                quota=settings.OPENAI_DAILY_QUOTA,
            ),
            notify(
                text=(
                    '☑️{}\n'
                    '◽️{}\n'
                    '◽️{}\n'
                ).format(
                    _('Downloading file...'),
                    _('Extracting text...'),
                    _('Summarizing...'),
                ),
            ),
            DownloadTelegramFile(
                token=settings.TELEGRAM_TOKEN,
                user_id=user_id,
            ),
            notify(
                text=(
                    '✅{}\n'
                    '☑️{}\n'
                    '◽️{}\n'
                ).format(
                    _('Download complete'),
                    _('Extracting text...'),
                    _('Summarizing...')
                ),
            ),
            ReadFile(),
            notify(
                text=(
                    '✅{}\n'
                    '✅{}\n'
                    '☑️{}\n'
                ).format(
                    _('Download complete'),
                    _('Text is extracted'),
                    _('Summarizing...'),
                ),
            ),
            SplitByTokensLength(
                max_tokens=settings.MAX_TOKENS_PER_PART,
                max_parts=settings.MAX_TEXT_PARTS,
                file_id=file_id,
            ),
            SummarizeChunks(summarize_stage=summarize_text),
            IfStage(
                condition=lambda data: len(data['content']) > 1,
                true_stage=Pipeline(
                    stages=[
                        JoinText(),
                        SplitByTokensLength(
                            max_tokens=settings.MAX_TOKENS_PER_PART,
                            max_parts=1,
                        ),
                        summarize_text,
                    ],
                ),
                false_stage=Idle(),
            ),
            JoinText(),
            notify(
                text=(
                    '✅{}\n'
                    '✅{}\n'
                    '✅{}\n'
                ).format(
                    _('Download complete'),
                    _('Text is extracted'),
                    _('Summarizing completed'),
                ),
            ),
        ],
    )

    try:
        return await summarize_pipeline(data={'file_id': file_id, 'telegram_file_id': telegram_file_id})
    except StopPipeline as e:
        await notify(f'😢 {e}')(data=None)
        return {
            'content': '',
        }
