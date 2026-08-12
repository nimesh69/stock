from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import BehaviorSummary, NewsPriceCorrelation


@admin.register(BehaviorSummary)
class BehaviorSummaryAdmin(ModelAdmin):
    list_display = (
        "company",
        "date",
        "close",
        "vwap",
        "pressure_indicator",
        "is_volume_anomaly",
        "computed_at",
    )
    list_filter = ("pressure_indicator", "is_volume_anomaly", "date", "computed_at")
    search_fields = ("company__symbol", "company__name")
    autocomplete_fields = ("company",)
    ordering = ("-date", "company__symbol")
    readonly_fields = ("computed_at",)


@admin.register(NewsPriceCorrelation)
class NewsPriceCorrelationAdmin(ModelAdmin):
    list_display = (
        "company",
        "window_start",
        "window_end",
        "correlation_coefficient",
        "news_count",
        "price_change_pct",
        "volume_change_pct",
        "computed_at",
    )
    list_filter = ("window_start", "window_end", "computed_at")
    search_fields = ("company__symbol", "company__name")
    autocomplete_fields = ("company",)
    ordering = ("-window_end", "company__symbol")
    readonly_fields = ("computed_at",)
