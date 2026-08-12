from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import CrawlRun


@admin.register(CrawlRun)
class CrawlRunAdmin(ModelAdmin):
    list_display = ("source", "status", "triggered_by", "started_at", "finished_at")
    list_filter = ("status", "source", "started_at", "finished_at")
    search_fields = ("source", "triggered_by__username", "triggered_by__email")
    autocomplete_fields = ("triggered_by",)
    ordering = ("-started_at",)
