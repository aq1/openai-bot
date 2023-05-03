from django.db import models


class Message(models.Model):
    message_id = models.PositiveBigIntegerField(
        help_text='Unique message identifier inside this chat',
    )

    chat = models.ForeignKey(
        to='bot.Chat',
        on_delete=models.CASCADE,
        related_name='messages',
    )

    user = models.ForeignKey(
        to='bot.TelegramUser',
        on_delete=models.CASCADE,
        related_name='messages',
    )

    text = models.TextField(
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
        return f'Message {self.message_id}'
