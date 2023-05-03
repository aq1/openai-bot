from django.db import models


class File(models.Model):

    id = models.CharField(
        max_length=100,
        primary_key=True,
    )

    telegram_file_id = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    user = models.ForeignKey(
        to='bot.TelegramUser',
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=1000,
        default='',
        blank=True,
    )

    content = models.FileField(
        upload_to='files',
        null=True,
        blank=True,
    )

    tokens = models.PositiveIntegerField(
        default=0,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title}'
