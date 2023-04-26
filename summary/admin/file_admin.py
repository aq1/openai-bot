from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ..models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user',
        )
