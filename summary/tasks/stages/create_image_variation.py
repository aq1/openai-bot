from typing import TypedDict

import openai
from django.utils.translation import gettext as _

from ...open_ai.request import create_image_variation
from .exceptions import StopPipeline
from .stage import Stage


class In(TypedDict):
    image: bytes
    prompt: str


class Out(TypedDict):
    prompt: str
    url: str


class CreateImageVariation(Stage[In, Out]):

    def __init__(self, user_id: int, n: int, size: str):
        self.user_id = user_id
        self.n = n
        self.size = size

    async def __call__(self, data: In) -> Out:
        try:
            url = (await create_image_variation(
                user_id=self.user_id,
                image=data['image'],
                n=self.n,
                size=self.size,
            ))['data'][0]['url']
        except (KeyError, IndexError, openai.OpenAIError):
            raise StopPipeline(_('😥 Sorry, could not process your request'))

        return {
            'prompt': data['prompt'],
            'url': url,
        }
