from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Company, CompanyEmbedding, DailyPrice, FloorsheetTransaction


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ("symbol", "name", "sector", "created_at")
    list_filter = ("sector", "created_at")
    search_fields = ("symbol", "name", "sector", "aliases")
    ordering = ("symbol",)
    readonly_fields = ("created_at",)


@admin.register(DailyPrice)
class DailyPriceAdmin(ModelAdmin):
    list_display = ("company", "date", "open", "high", "low", "close", "volume", "turnover")
    list_filter = ("date",)
    search_fields = ("company__symbol", "company__name")
    autocomplete_fields = ("company",)
    ordering = ("-date", "company__symbol")


@admin.register(FloorsheetTransaction)
class FloorsheetTransactionAdmin(ModelAdmin):
    list_display = ("company", "date", "buyer_broker", "seller_broker", "quantity", "rate")
    list_filter = ("date", "buyer_broker", "seller_broker")
    search_fields = ("company__symbol", "company__name", "buyer_broker", "seller_broker")
    autocomplete_fields = ("company",)
    ordering = ("-date", "company__symbol")


@admin.register(CompanyEmbedding)
class CompanyEmbeddingAdmin(ModelAdmin):
    list_display = ("company", "created_at", "updated_at")
    search_fields = ("company__symbol", "company__name", "source_text")
    autocomplete_fields = ("company",)
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")
