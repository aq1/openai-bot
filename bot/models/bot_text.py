from django.db import models


class BotText(models.Model):
    label = models.CharField(
        max_length=32,
        primary_key=True,
    )

    ru = models.TextField(
        help_text='Russian text',
    )

    en = models.TextField(
        help_text='English text',
    )

    def __str__(self):
        return f'{self.label}'

