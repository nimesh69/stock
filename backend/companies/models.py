from django.db import models


class Company(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100, blank=True)

    aliases = models.JSONField(default=list, blank=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} — {self.name}"


class DailyPrice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()
    turnover = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        unique_together = ("company", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.company.symbol} {self.date}"


# Optional — only needed if you end up sampling floorsheet data.
# Not required for the 10-hour scope; safe to leave unmigrated/unused.
class FloorsheetTransaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="floorsheet_entries")
    date = models.DateField()
    buyer_broker = models.CharField(max_length=100)
    seller_broker = models.CharField(max_length=100)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        indexes = [models.Index(fields=["company", "date"])]
        
from pgvector.django import VectorField


class CompanyEmbedding(models.Model):

    company = models.OneToOneField(
        Company,
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

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Embedding: {self.company.symbol}"