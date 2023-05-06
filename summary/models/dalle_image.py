from django.db import models


class DalleImage(models.Model):
    user = models.ForeignKey(
        to='bot.TelegramUser',
        on_delete=models.RESTRICT,
    )

    prompt = models.TextField(
        default='',
        blank=True,
    )

    image = models.ImageField(
        upload_to='dalle/%Y/%m/%d/',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'Image by {self.user}'
