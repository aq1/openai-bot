from typing import TypedDict

from django.conf import settings

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
)


class In(TypedDict):
    telegram_file_id: str


class Out(TypedDict):
    telegram_file_id: str


async def summarize_file(file_id: str, telegram_file_id: str, language: str, chat_id: int, message_id: int):
    summarize_pipeline: Pipeline[In, Out] = Pipeline(
        stages=[
            DownloadTelegramFile(
                token=settings.TELEGRAM_TOKEN,
            ),
            ReadFile(),
            SplitByTokensLength(
                max_tokens=settings.MAX_TOKENS_PER_PART,
                max_parts=settings.MAX_TEXT_PARTS,
            ),
            SummarizeChunks(language=language),
            IfStage(
                condition=lambda data: len(data['content']) > 1,
                true_stage=Pipeline(
                    stages=[
                        JoinText(),
                        SplitByTokensLength(
                            max_tokens=settings.MAX_TOKENS_PER_PART,
                            max_parts=1,
                        ),
                        SummarizeText(language=language),
                    ]
                ),
                false_stage=Idle()
            ),
            JoinText(),
        ]
    )

    result = await summarize_pipeline(data={'file_id': file_id, 'telegram_file_id': telegram_file_id})

    return result['content']
