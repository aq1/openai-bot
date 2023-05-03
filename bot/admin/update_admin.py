from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ..models import Update


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
    )

    search_fields = (
        'id',
    )

    ordering = (
        '-id',
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }
