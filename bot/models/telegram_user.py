from django.db import models
from django.conf import settings


class TelegramUser(models.Model):

    is_bot = models.BooleanField(
        blank=True,
    )

    is_premium = models.BooleanField(
        blank=True,
        default=False,
    )

    groups = models.ManyToManyField(
        to='auth.Group',
        related_name='telegram_users',
    )

    first_name = models.CharField(
        max_length=255,
    )

    last_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    username = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    language = models.CharField(
        max_length=5,
        default=settings.DEFAULT_LANGUAGE,
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
        return f'User {self.id} {self.username or self.first_name}'
