from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import CrawlerProcess

from crawler.spiders.sharesansar_news import ShareSansarNewsSpider
from crawler.spiders.sharesansar_prices import ShareSansarPricesSpider


SPIDERS = {
    "sharesansar_news": ShareSansarNewsSpider,
    "sharesansar_prices": ShareSansarPricesSpider,
}


class Command(BaseCommand):
    help = "Run a Scrapy spider."

    def add_arguments(self, parser):
        parser.add_argument(
            "spider_name",
            choices=SPIDERS.keys(),
        )

    def handle(self, *args, **options):
        spider_name = options["spider_name"]
        spider_class = SPIDERS[spider_name]

        process = CrawlerProcess(
            settings={
                "ROBOTSTXT_OBEY": True,
                "DOWNLOAD_DELAY": 2,
                "USER_AGENT": (
                    "StockAppAssignmentCrawler/1.0 "
                    "(+contact: nimeshstha79@gmail.com)"
                ),
                "ITEM_PIPELINES": {
                    "crawler.pipelines.DjangoWritePipeline": 300,
                    "crawler.pipelines.DailyPricePipeline": 400,
                },
                "LOG_LEVEL": "INFO",
            }
        )

        self.stdout.write(
            f"Starting spider: {spider_name}"
        )

        process.crawl(spider_class)
        process.start()

        self.stdout.write(
            self.style.SUCCESS(
                f"Spider {spider_name} finished."
            )
        )