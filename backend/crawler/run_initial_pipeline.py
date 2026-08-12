import os
import sys

sys.path.insert(0, "/backend")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stock.settings")

import django

django.setup()

from celery import chain
from Stock.celery import app

from crawler.tasks import (
    crawl_share_prices,
    crawl_share_news,
    generate_embeddings_task,
)

from analysis.tasks import compute_behavior_summary_all_companies


days_back = 30

pipeline = chain(
    crawl_share_prices.si(days_back=days_back),
    compute_behavior_summary_all_companies.si(),
    crawl_share_news.si(days_back=days_back),
    generate_embeddings_task.si(),
)

result = pipeline.apply_async()

print(f"Pipeline task started: {result.id}")
print(f"Result backend: {result.backend}")
print("Waiting for pipeline to finish...")

result.get(
    timeout=None,
    disable_sync_subtasks=False,
)

print("Pipeline completed successfully.")