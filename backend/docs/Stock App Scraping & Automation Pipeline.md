# Stock App Scraping & Automation Pipeline

This document explains how the data crawling, processing, and scheduled execution pipeline works across Docker containers using Scrapy, Celery, and Django.

---

## 1. Pipeline Overview

When the application starts for the first time, it runs a **30-day historical backfill**. Once completed, it transitions to a **daily 1-day sync** running automatically via Celery Beat.

```text
[ Container Startup ] ──> Initial 30-Day Pipeline ──> Seeded & Ready
                                                         │
[ Daily Cron @ 5 PM NPT ] ──────────────────────────────┴──> 1-Day Incremental Sync
```

---

## 2. Pipeline Stages

The full data pipeline (`crawler.tasks.run_full_pipeline`) runs sequentially via a Celery `chain`:

1. **`crawl_share_prices`**: Crawls price history using `ShareSansarPricesSpider`.
2. **`compute_behavior_summary_all_companies`**: Calculates technical metrics and summaries based on newly updated prices.
3. **`crawl_share_news`**: Scrapes recent news articles using `ShareSansarNewsSpider`.
4. **`categorize_news_by_embeddings`**: Generates news embeddings and categorizes articles using AI vector search.

---

## 3. Crawl Strategy (`days_back`)

Both spiders accept a dynamic `days_back` parameter to control the depth of historical fetching.

| Parameter Value | Price Spider Behavior | News Spider Behavior |
| :--- | :--- | :--- |
| **`days_back = 30`** | Fetches today's prices + 29 previous days (30 days total). | Scrapes articles published up to 30 days ago. |
| **`days_back = 1`** | Fetches only today's price table. | Scrapes articles published in the last 24 hours. |

### Spider Core Implementation

#### Prices (`ShareSansarPricesSpider`)

```python
for i in range(1, self.days_back):
    target_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    # POST request for historical AJAX table
```

#### News (`ShareSansarNewsSpider`)

```python
if published_at and datetime.now() - published_at > timedelta(days=self.days_back):
    stop_paginating = True
```

---

## 4. Execution Workflow

### A. First-Time Application Launch (30 Days)

1. Docker spins up the `init-db` service to:
   - Apply migrations.
   - Seed static company data.
   - Build company embeddings.

2. `web`, `frontend`, and `celery-worker` launch and are immediately usable.

3. `celery-startup` dispatches the initial 30-day crawl job:

```bash
celery -A Stock call crawler.tasks.run_full_pipeline --kwargs='{"days_back": 30}'
```

4. A marker file (`/startup-data/initial_crawl_done`) is created.

5. On future container restarts, the 30-day initial crawl is skipped.

---

### B. Daily Scheduled Sync (1 Day)

Celery Beat is configured in `settings.py` to trigger the pipeline automatically every day at **5:00 PM Nepal Time (UTC+5:45)** with the default `days_back=1`.

```python
# settings.py

CELERY_TIMEZONE = "Asia/Kathmandu"

CELERY_BEAT_SCHEDULE = {
    "daily-full-pipeline": {
        "task": "crawler.tasks.run_full_pipeline",
        "schedule": crontab(hour=17, minute=0),  # 5:00 PM NPT
        "kwargs": {"days_back": 1},
    },
}
```

---

## 5. Manual CLI Execution

You can trigger spiders or the full pipeline manually at any time with custom timeframes using Django management commands or the Celery CLI.

### Run Django Management Command Directly

#### Crawl 7 Days of News

```bash
python manage.py crawl_spider sharesansar_news --days_back 7
```

#### Crawl 1 Day of Prices

```bash
python manage.py crawl_spider sharesansar_prices --days_back 1
```

### Dispatch Celery Task Manually

#### Enqueue Full Pipeline for 14 Days

```bash
celery -A Stock call crawler.tasks.run_full_pipeline --kwargs='{"days_back": 14}'
```