from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ArticleCategory, ArticleEmbedding, CategoryCorrection, RawArticle


@admin.register(RawArticle)
class RawArticleAdmin(ModelAdmin):
    list_display = ("headline", "source_portal", "published_at", "scraped_at")
    list_filter = ("source_portal", "published_at", "scraped_at")
    search_fields = ("headline", "body", "url")
    ordering = ("-published_at", "-scraped_at")
    readonly_fields = ("scraped_at",)


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(ModelAdmin):
    list_display = ("article", "company", "confidence", "method", "created_at")
    list_filter = ("method", "company", "created_at")
    search_fields = ("article__headline", "company__symbol", "company__name")
    autocomplete_fields = ("article", "company")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(CategoryCorrection)
class CategoryCorrectionAdmin(ModelAdmin):
    list_display = (
        "article_category",
        "previous_company",
        "new_company",
        "corrected_by",
        "corrected_at",
    )
    list_filter = ("new_company", "previous_company", "corrected_at")
    search_fields = (
        "article_category__article__headline",
        "previous_company__symbol",
        "new_company__symbol",
        "corrected_by__username",
        "corrected_by__email",
        "reason",
    )
    autocomplete_fields = ("article_category", "previous_company", "new_company", "corrected_by")
    ordering = ("-corrected_at",)
    readonly_fields = ("corrected_at",)


@admin.register(ArticleEmbedding)
class ArticleEmbeddingAdmin(ModelAdmin):
    list_display = ("article", "created_at")
    search_fields = ("article__headline", "source_text")
    autocomplete_fields = ("article",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
