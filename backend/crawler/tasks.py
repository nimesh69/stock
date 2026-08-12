import subprocess
import sys

from celery import chain, shared_task

from analysis.tasks import compute_behavior_summary_all_companies


def run_crawler(spider_name, days_back):
    result = subprocess.run(
        [
            sys.executable,
            "manage.py",
            "crawl_spider",
            spider_name,
            "--days_back",
            str(days_back),
        ],
        cwd="/backend",
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Spider '{spider_name}' failed.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return result.stdout


@shared_task
def crawl_share_prices(days_back=1):
    run_crawler("sharesansar_prices", days_back)
    return f"share prices crawled for {days_back} day(s)"


@shared_task
def crawl_share_news(days_back=1):
    run_crawler("sharesansar_news", days_back)
    return f"share news crawled for {days_back} day(s)"


@shared_task
def generate_embeddings_task():
    from django.core.management import call_command

    call_command("categorize_news_by_embeddings")
    return "news embeddings generated and categorized"



def full_pipeline(days_back=1):
    return chain(
        crawl_share_prices.si(days_back=days_back),
        compute_behavior_summary_all_companies.si(),
        crawl_share_news.si(days_back=days_back),
        generate_embeddings_task.si(),
    ).apply_async()

@shared_task
def start_full_pipeline(days_back=1):
    return full_pipeline(days_back)