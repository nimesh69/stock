from celery import shared_task, chain
from django.core.management import call_command

from analysis.tasks import compute_behavior_summary_all_companies


@shared_task
def crawl_share_prices():
    call_command("crawl_spider", "sharesansar_prices")
    return "share prices crawled"


@shared_task
def crawl_share_news():
    call_command("crawl_spider", "sharesansar_news")
    call_command("categorize_news_by_embeddings")
    return "share news crawled, embedded, and categorized"


@shared_task
def generate_embeddings_task():
    call_command("categorize_news_by_embeddings")
    return "news embeddings generated and categorized"


@shared_task
def run_full_pipeline():
    """Crawl prices -> compute behavior summary -> crawl news -> categorize, in order."""
    chain(
        crawl_share_prices.si(),
        compute_behavior_summary_all_companies.si(),
        crawl_share_news.si(),
    ).apply_async()

    return "Full pipeline started"