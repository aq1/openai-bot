from django.utils.translation import gettext as _

from .stage import Stage
from .exceptions import StopPipeline


class CheckLength(Stage):
    def __init__(self, min_length: int):
        self.min_length = min_length

    async def __call__(self, data):
        if len(data['content']) <= self.min_length:
            raise StopPipeline(_('🤔 This text looks too short. It probably does not need to be summarized.'))

        return data
