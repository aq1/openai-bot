from django.contrib import admin

from ..models import BotText


@admin.register(BotText)
class BotTextAdmin(admin.ModelAdmin):
    list_display = (
        'label',
        'ru',
    )
