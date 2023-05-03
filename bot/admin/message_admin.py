from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ..models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'chat',
        'user',
        'updated_at',
    )

    search_fields = (
        'id',
    )

    ordering = (
        '-updated_at',
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'chat',
            'user',
        )
