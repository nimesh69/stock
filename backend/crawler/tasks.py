# crawler/tasks.py
import subprocess
from pathlib import Path

from celery import shared_task, chain
from django.core.management import call_command

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # adjust to your scrapy.cfg location


def _run_spider(spider_name: str):
    result = subprocess.run(
        ["scrapy", "crawl", spider_name],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Spider {spider_name} failed:\n{result.stderr}")
    return result.stdout


@shared_task
def crawl_share_prices():
    return _run_spider("sharesansar_prices")


@shared_task
def crawl_share_news():
    return _run_spider("sharesansar_news")


@shared_task
def generate_embeddings_task():
    call_command("generate_embeddings")
    return "embeddings generated"


@shared_task
def run_full_pipeline():
    """Crawl prices -> crawl news -> generate embeddings, in order."""
    chain(
        crawl_share_prices.si(),
        crawl_share_news.si(),
        generate_embeddings_task.si(),
    ).apply_async()