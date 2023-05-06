from typing import TypedDict

from django.utils.translation import gettext as _

from .stage import (
    Stage,
)

from .exceptions import (
    StopPipeline,
)

from ...models import (
    DalleImage,
)


class In(TypedDict):
    file_id: int


class Out(TypedDict):
    image: bytes
    prompt: str


class LoadImageFromDb(Stage[In, Out]):
    async def __call__(self, data: In) -> Out:
        db_image = await DalleImage.objects.filter(
            id=data['file_id'],
        ).afirst()

        if not db_image:
            raise StopPipeline(_('Image was not found'))

        return {
            'image': db_image.image.read(),
            'prompt': db_image.prompt,
        }
