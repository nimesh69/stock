# Behavior Summary & Market Pressure Indicator

## Overview

The system generates a daily `BehaviorSummary` for each company using price and volume data.

It calculates:

* **20-day Rolling VWAP**
* **20-day Average Volume**
* **Price Change**
* **Pressure Indicator**
* **Volume Anomaly**

## 1. Pressure Indicator

`compute_pressure_indicator()` compares daily price movement with average volume.

| Condition                     | Indicator      |
| ----------------------------- | -------------- |
| Price change < 0.2%           | `neutral`      |
| Price up + volume ≥ average   | `accumulation` |
| Price up + volume < average   | `weak_rally`   |
| Price down + volume ≥ average | `distribution` |
| Price down + volume < average | `weak_selloff` |

If average volume is missing or zero, the result is `neutral`.

## 2. Rolling VWAP

`compute_rolling_vwap()` calculates VWAP over the trailing **20 trading days**.

**Formula:**

```text
Typical Price = (High + Low + Close) / 3

VWAP = Σ(Typical Price × Volume) / Σ(Volume)
```

The result is rounded to **2 decimal places**.

Returns `None` when there is no data or total volume is zero.

## 3. Volume Anomaly

A volume anomaly is detected when:

```text
Today's Volume >= 2 × 20-Day Average Volume
```

This is controlled by:

```python
ANOMALY_MULTIPLIER = Decimal("2.0")
```

## 4. Daily Summary Process

For each company, the Celery task:

1. Finds the latest available trading date.
2. Gets the trailing 20 trading days.
3. Calculates VWAP and average volume.
4. Calculates price change from the previous trading day.
5. Determines the pressure indicator.
6. Detects volume anomalies.
7. Creates or updates `BehaviorSummary`.

The summary is uniquely maintained by:

```text
(company, date)
```

using `update_or_create()`.

## 5. All Companies

`compute_behavior_summary_all_companies()` queues a separate Celery task for every company, allowing summaries to be calculated asynchronously.

## Key Configuration

| Setting                   |           Value |
| ------------------------- | --------------: |
| VWAP / Volume window      | 20 trading days |
| Flat price threshold      |            0.2% |
| Volume anomaly multiplier |              2× |
