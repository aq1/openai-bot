from django.db import models
from django.db.models import functions
from django.utils import timezone
from django.utils.translation import gettext as _, activate

from .stage import Stage
from .exceptions import StopPipeline

from ...models import OpenAICall


class CheckLength(Stage):
    def __init__(self, min_length: int):
        self.min_length = min_length

    async def __call__(self, data):
        if len(data['content']) <= self.min_length:
            raise StopPipeline(_('🤔 This text looks too short. It probably does not need to be summarized.'))

        return data
