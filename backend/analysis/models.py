from django.db import models

from companies.models import Company


class BehaviorSummary(models.Model):
    PRESSURE_CHOICES = [
        ("accumulation", "Accumulation"),
        ("distribution", "Distribution"),
        ("weak_rally", "Weak rally"),
        ("weak_selloff", "Weak selloff"),
        ("neutral", "Neutral"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="behavior_summaries")
    date = models.DateField()
    vwap = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    pressure_indicator = models.CharField(max_length=20, choices=PRESSURE_CHOICES)
    is_volume_anomaly = models.BooleanField(default=False)
    avg_volume_20d = models.BigIntegerField(null=True, blank=True)
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.company.symbol} {self.date} — {self.pressure_indicator}"


# Optional / stretch — only build this out if VWAP + pressure + anomaly are
# already solid and time remains. Safe to skip for the 10-hour scope.
class NewsPriceCorrelation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="news_correlations")
    window_start = models.DateField()
    window_end = models.DateField()
    correlation_coefficient = models.FloatField()
    news_count = models.IntegerField()
    price_change_pct = models.FloatField()
    volume_change_pct = models.FloatField()
    computed_at = models.DateTimeField(auto_now=True)