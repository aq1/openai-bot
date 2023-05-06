from typing import TypedDict

from django.utils.translation import gettext as _

from ..models import DalleImage
from .stages.exceptions import (
    StopPipeline,
)
from .stages import (
    Pipeline,
    GenerateImage,
    TelegramNotification, SaveImage, LoadImageFromDb, CreateImageVariation,
)


class In(TypedDict):
    file_id: int


class Out(TypedDict):
    url: str
    db_image: DalleImage


async def create_image_variation(
        bot_token: str,
        user_id: int,
        file_id: int,
        chat_id: int,
        message_id: int,
) -> Out:
    notify = TelegramNotification(
        token=bot_token,
        chat_id=chat_id,
        message_id=message_id,
    )

    create_image_variation_pipeline: Pipeline[In, Out] = Pipeline(
        stages=[
            notify(
                text=(
                    '☑️{}\n'
                ).format(
                    _('Generating...'),
                ),
            ),
            LoadImageFromDb(),
            CreateImageVariation(
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
        ]
    )

    try:
        return await create_image_variation_pipeline(data={'file_id': file_id})
    except StopPipeline as e:
        await notify(str(e))(data=None)
        return {
            'url': '',
            'db_image': DalleImage(),
        }
