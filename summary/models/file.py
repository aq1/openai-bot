from django.db import models


class File(models.Model):

    file_id = models.CharField(
        max_length=100,
        primary_key=True,
    )

    user = models.ForeignKey(
        to='bot.User',
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=1000,
    )

    content = models.FileField(
        upload_to='files',
    )

    summary = models.JSONField(
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title}'
