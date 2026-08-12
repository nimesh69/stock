from celery import chain, shared_task
from django.core.management import call_command

from analysis.tasks import compute_behavior_summary_all_companies


@shared_task
def crawl_share_prices(days_back=1):
    call_command("crawl_spider", "sharesansar_prices", days_back=days_back)
    compute_behavior_summary_all_companies.delay()
    return f"share prices crawled for {days_back} day(s)"


@shared_task
def crawl_share_news(days_back=1):
    call_command("crawl_spider", "sharesansar_news", days_back=days_back)
    call_command("categorize_news_by_embeddings")
    return f"share news crawled ({days_back} day(s)), embedded, and categorized"


@shared_task
def generate_embeddings_task():
    call_command("categorize_news_by_embeddings")
    return "news embeddings generated and categorized"


@shared_task
def run_full_pipeline(days_back=1):
    """Crawl prices -> compute behavior summary -> crawl news -> categorize, in order."""
    chain(
        crawl_share_prices.si(days_back=days_back),
        compute_behavior_summary_all_companies.si(),
        crawl_share_news.si(days_back=days_back),
        generate_embeddings_task.si(),
    ).apply_async()

    return f"Full pipeline started with days_back={days_back}"