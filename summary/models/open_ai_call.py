from django.db import models


class OpenAICall(models.Model):
    request = models.JSONField(
        default=dict,
        blank=True,
    )

    response = models.JSONField(
        default=dict,
        blank=True,
    )

    tokens = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'OpenAI call: {self.tokens}'
