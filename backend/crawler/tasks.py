import subprocess
import sys

from celery import chain, shared_task
from django.core.management import call_command

from analysis.tasks import compute_behavior_summary_all_companies


def run_scrapy(spider, days_back):
    subprocess.run(
        [
            sys.executable,
            "manage.py",
            "crawl_spider",
            spider,
            "--days-back",
            str(days_back),
        ],
        check=True,
    )


@shared_task
def crawl_share_prices(days_back=1):
    run_scrapy("sharesansar_prices", days_back)

    return f"share prices crawled for {days_back} day(s)"


@shared_task
def crawl_share_news(days_back=1):
    run_scrapy("sharesansar_news", days_back)

    return f"share news crawled for {days_back} day(s)"


@shared_task
def generate_embeddings_task():
    call_command("categorize_news_by_embeddings")

    return "news embeddings generated and categorized"


@shared_task
def run_full_pipeline(days_back=1):
    pipeline = chain(
        crawl_share_prices.si(days_back=days_back),
        compute_behavior_summary_all_companies.si(),
        crawl_share_news.si(days_back=days_back),
        generate_embeddings_task.si(),
    )

    pipeline.apply_async()

    return f"Full pipeline started with days_back={days_back}"


