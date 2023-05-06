from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class BytesEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return '[bytes]'

        return super().default(o)


class OpenAICall(models.Model):
    user = models.ForeignKey(
        to='bot.TelegramUser',
        on_delete=models.RESTRICT,
    )

    request = models.JSONField(
        default=dict,
        blank=True,
        encoder=BytesEncoder,
    )

    response = models.JSONField(
        default=dict,
        blank=True,
        encoder=BytesEncoder,
    )

    tokens = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'OpenAI call: {self.tokens}'
