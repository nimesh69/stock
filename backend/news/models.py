from django.conf import settings
from django.db import models

from companies.models import Company
from pgvector.django import VectorField


class RawArticle(models.Model):
    source_portal = models.CharField(max_length=50)
    headline = models.CharField(max_length=500)
    body = models.TextField()
    url = models.URLField(unique=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline[:80]


class ArticleCategory(models.Model):

    METHOD_CHOICES = [
        ("embedding", "Embedding similarity"),
        ("manual", "Manual"),
    ]

    article = models.ForeignKey(
        RawArticle,
        on_delete=models.CASCADE,
        related_name="categories",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="article_categories",
    )

    confidence = models.FloatField()

    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default="hybrid",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "company"],
                name="unique_article_company_category",
            )
        ]


class CategoryCorrection(models.Model):
    article_category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name="corrections")
    corrected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    previous_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name="+", blank=True
    )
    new_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="+")
    reason = models.TextField(blank=True)
    corrected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correction on ArticleCategory {self.article_category_id}"
    
class ArticleEmbedding(models.Model):

    article = models.OneToOneField(
        RawArticle,
        on_delete=models.CASCADE,
        related_name="embedding",
    )

    embedding = VectorField(
        dimensions=384
    )

    source_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )