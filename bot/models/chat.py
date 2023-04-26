from django.db import models


class Chat(models.Model):

    type = models.CharField(
        max_length=255,
        blank=True,
    )

    title = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    username = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
    )

    data = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f'Chat {self.id} {self.title or self.username}'
