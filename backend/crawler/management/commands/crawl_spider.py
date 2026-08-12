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
        # Added --days_back argument (optional, defaults to 1)
        parser.add_argument(
            "--days_back",
            type=int,
            default=1,
            help="Number of historical days to crawl (default: 1)",
        )

    def handle(self, *args, **options):
        spider_name = options["spider_name"]
        days_back = options["days_back"]
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
            f"Starting spider: {spider_name} with days_back={days_back}"
        )

        # Pass days_back as a keyword argument to the spider's __init__
        process.crawl(spider_class, days_back=days_back)
        process.start()

        self.stdout.write(
            self.style.SUCCESS(
                f"Spider {spider_name} finished."
            )
        )