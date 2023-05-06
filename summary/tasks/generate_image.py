from typing import TypedDict

from django.utils.translation import gettext as _

from ..models import DalleImage
from .stages.exceptions import (
    StopPipeline,
)
from .stages import (
    Pipeline,
    GenerateImage,
    TelegramNotification, SaveImage,
)


class In(TypedDict):
    prompt: str


class Out(TypedDict):
    url: str
    db_image: DalleImage


async def generate_image(
        bot_token: str,
        user_id: int,
        prompt: str,
        chat_id: int,
        message_id: int,
) -> Out:
    notify = TelegramNotification(
        token=bot_token,
        chat_id=chat_id,
        message_id=message_id,
    )

    generate_image_pipeline: Pipeline[In, Out] = Pipeline(
        stages=[
            notify(
                text=(
                    '☑️{}\n'
                ).format(
                    _('Generating...'),
                ),
            ),
            GenerateImage(
                user_id=user_id,
                n=1,
                size='512x512',
            ),
            SaveImage(
                user_id=user_id,
            ),
            notify(
                text=(
                    '✅{}\n'
                ).format(
                    _('Image created'),
                ),
            ),
        ],
    )

    try:
        return await generate_image_pipeline(data={'prompt': prompt})
    except StopPipeline as e:
        await notify(str(e))(data=None)
        return {
            'url': '',
            'db_image': DalleImage(),
        }
