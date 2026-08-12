from decimal import Decimal

ANOMALY_MULTIPLIER = Decimal("2.0")
PRICE_CHANGE_THRESHOLD = Decimal("0.002")  # 0.2% — treated as "flat" below this


def compute_pressure_indicator(price_change_pct: Decimal, volume: int, avg_volume_20d: int | None) -> str:
    if avg_volume_20d is None or avg_volume_20d == 0:
        return "neutral"

    volume_ratio = Decimal(volume) / Decimal(avg_volume_20d)
    above_avg_volume = volume_ratio >= Decimal("1.0")

    if abs(price_change_pct) < PRICE_CHANGE_THRESHOLD:
        return "neutral"

    if price_change_pct > 0:
        return "accumulation" if above_avg_volume else "weak_rally"
    else:
        return "distribution" if above_avg_volume else "weak_selloff"


def compute_rolling_vwap(price_rows: list) -> Decimal | None:
    """
    price_rows: list of DailyPrice-like objects with .high, .low, .close, .volume,
    ordered ascending by date, representing the trailing window (e.g. 20 days)
    ending on the target date (inclusive).
    """
    if not price_rows:
        return None

    total_pv = Decimal("0")
    total_volume = 0

    for row in price_rows:
        typical_price = (row.high + row.low + row.close) / Decimal("3")
        total_pv += typical_price * row.volume
        total_volume += row.volume

    if total_volume == 0:
        return None

    return (total_pv / Decimal(total_volume)).quantize(Decimal("0.01"))