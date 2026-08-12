from celery import shared_task
from django.db.models import Avg
from datetime import timedelta

from companies.models import Company, DailyPrice
from .models import BehaviorSummary
from .utils import compute_pressure_indicator, compute_rolling_vwap, ANOMALY_MULTIPLIER

WINDOW_DAYS = 20


@shared_task
def compute_behavior_summary_for_company(company_id, target_date=None):
    company = Company.objects.get(pk=company_id)

    prices_qs = DailyPrice.objects.filter(company=company).order_by("date")
    if target_date:
        prices_qs = prices_qs.filter(date__lte=target_date)

    today_price = prices_qs.last()
    if not today_price:
        return

    target_date = today_price.date

    window_start = target_date - timedelta(days=WINDOW_DAYS * 2)  # buffer for weekends/holidays
    window_rows = list(
        DailyPrice.objects.filter(
            company=company, date__lte=target_date, date__gte=window_start
        ).order_by("date")[:WINDOW_DAYS]
    ) or list(
        DailyPrice.objects.filter(company=company, date__lte=target_date)
        .order_by("-date")[:WINDOW_DAYS][::-1]
    )

    avg_volume_20d = (
        DailyPrice.objects.filter(company=company, date__lte=target_date)
        .order_by("-date")[:WINDOW_DAYS]
        .aggregate(avg=Avg("volume"))["avg"]
    )
    avg_volume_20d = int(avg_volume_20d) if avg_volume_20d else None

    prev_price = (
        DailyPrice.objects.filter(company=company, date__lt=target_date)
        .order_by("-date")
        .first()
    )
    price_change_pct = (
        (today_price.close - prev_price.close) / prev_price.close
        if prev_price and prev_price.close
        else 0
    )

    vwap = compute_rolling_vwap(window_rows)
    pressure = compute_pressure_indicator(price_change_pct, today_price.volume, avg_volume_20d)
    is_anomaly = (
        avg_volume_20d is not None
        and today_price.volume >= avg_volume_20d * ANOMALY_MULTIPLIER
    )

    BehaviorSummary.objects.update_or_create(
        company=company,
        date=target_date,
        defaults={
            "vwap": vwap,
            "close": today_price.close,
            "pressure_indicator": pressure,
            "is_volume_anomaly": is_anomaly,
            "avg_volume_20d": avg_volume_20d,
        },
    )


@shared_task
def compute_behavior_summary_all_companies():
    for company_id in Company.objects.values_list("id", flat=True):
        compute_behavior_summary_for_company.delay(company_id)