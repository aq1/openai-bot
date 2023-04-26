from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ..models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'updated_at',
    )

    ordering = (
        '-updated_at',
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }
