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
    SummarizeText,
    SplitByTokensLength,
    JoinText,
    TelegramNotification,
    CheckQuota,
    CheckLength,
)


class In(TypedDict):
    content: str


class Out(TypedDict):
    content: str


async def summarize_text(
        user_id: int,
        text: str,
        language: str,
        chat_id: int,
        message_id: int,
) -> Out:
    notify = TelegramNotification(
        token=settings.TELEGRAM_TOKEN,
        chat_id=chat_id,
        message_id=message_id,
    )

    summarize_text_stage = SummarizeText(
        language=language,
        user_id=user_id,
    )

    summarize_pipeline: Pipeline[In, Out] = Pipeline(
        stages=[
            CheckQuota(
                user_id=user_id,
                quota=settings.OPENAI_DAILY_QUOTA,
            ),
            CheckLength(
                min_length=settings.MIN_TEXT_LENGTH,
            ),
            notify(
                text=(
                    '☑️{}\n'
                ).format(
                    _('Summarizing...'),
                ),
            ),
            SplitByTokensLength(
                max_tokens=settings.MAX_TOKENS_PER_PART,
                max_parts=settings.MAX_TEXT_PARTS,
            ),
            SummarizeChunks(summarize_stage=summarize_text_stage),
            IfStage(
                condition=lambda data: len(data['content']) > 1,
                true_stage=Pipeline(
                    stages=[
                        JoinText(),
                        SplitByTokensLength(
                            max_tokens=settings.MAX_TOKENS_PER_PART,
                            max_parts=1,
                        ),
                        summarize_text_stage,
                    ],
                ),
                false_stage=Idle(),
            ),
            JoinText(),
            notify(
                text=(
                    '✅{}\n'
                ).format(
                    _('Summarizing completed'),
                ),
            ),
        ],
    )

    try:
        return await summarize_pipeline(data={'content': text})
    except StopPipeline as e:
        await notify(str(e))(data=None)
        return {
            'content': '',
        }
