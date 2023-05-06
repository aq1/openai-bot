import io
from typing import TypedDict
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.utils.translation import gettext as _

from .exceptions import StopPipeline
from ...models import DalleImage

from .stage import Stage


class In(TypedDict):
    prompt: str
    url: str


class Out(TypedDict):
    url: str
    db_image: DalleImage


class SaveImage(Stage[In, Out]):

    def __init__(self, user_id: int):
        self.user_id = user_id

    async def __call__(self, data: In) -> Out:
        try:
            title = urlparse(data['url']).path.split('/')[-1]
        except IndexError:
            title = 'Untitled.png'

        _bytes = io.BytesIO()

        try:
            content = requests.get(data['url']).content
        except requests.RequestException:
            raise StopPipeline(_('Failed to download file'))

        _bytes.write(content)
        _bytes.seek(0)

        db_image = await DalleImage.objects.acreate(
            user_id=self.user_id,
            prompt=data['prompt'],
            image=ContentFile(
                content=_bytes.read(),
                name=title,
            ),
        )

        return {
            'url': data['url'],
            'db_image': db_image,
        }
