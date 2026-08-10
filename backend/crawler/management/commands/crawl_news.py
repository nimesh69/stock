"""
crawler/management/commands/crawl_news.py

Run with: python manage.py crawl_news

Since this runs inside manage.py, Django is already set up before this
executes — no sys.path/django.setup() dance needed. The pipeline can
import Django models directly.
"""
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from crawler.spiders.sharesansar_news import ShareSansarNewsSpider


class Command(BaseCommand):
    help = "Runs the sharesansar news spider and writes results to the database."

    def handle(self, *args, **options):
        process = CrawlerProcess(settings={
            "ROBOTSTXT_OBEY": True,
            "DOWNLOAD_DELAY": 2,
            "USER_AGENT": "StockAppAssignmentCrawler/1.0 (+contact: your-email@example.com)",
            "ITEM_PIPELINES": {
                "crawler.pipelines.DjangoWritePipeline": 300,
                "crawler.pipelines.DailyPricePipeline": 400,
            },
            "LOG_LEVEL": "INFO",
        })
        process.crawl(ShareSansarNewsSpider)
        process.start()  # blocks until the crawl finishes
        self.stdout.write(self.style.SUCCESS("Crawl finished."))