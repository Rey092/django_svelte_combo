"""Base admin."""

from unfold.admin import ModelAdmin


class BaseAdmin(ModelAdmin):
    """Base admin."""

    actions = None
    ordering = ["pk"]
