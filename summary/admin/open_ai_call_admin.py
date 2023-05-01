from django.conf import settings
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ..models import OpenAICall


@admin.register(OpenAICall)
class OpenAICallAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'tokens',
        'tokens_price',
    )

    ordering = (
        '-created_at',
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }

    @admin.display(description='Cost', ordering='tokens')
    def tokens_price(self, obj: OpenAICall):
        return round(obj.tokens * settings.TOKEN_PRICE, 4)
