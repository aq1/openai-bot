from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ..models import TelegramUser


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'updated_at',
    )

    ordering = (
        '-updated_at',
    )

    search_fields = (
        'id',
        'username',
        'first_name',
        'last_name',
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }
