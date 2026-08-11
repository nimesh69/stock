"""
crawler/pipelines.py

Pipelines for writing Scrapy items into Django/PostgreSQL.

Django ORM operations are wrapped with sync_to_async because
Scrapy processes items asynchronously.
"""

from datetime import datetime

from asgiref.sync import sync_to_async


class DjangoWritePipeline:

    async def process_item(self, item, spider):
        if spider.name != "sharesansar_news":
            return item

        await self.save_article(item)
        return item

    @sync_to_async
    def save_article(self, item):
        from news.models import RawArticle

        RawArticle.objects.get_or_create(
            url=item["url"],
            defaults={
                "headline": item["headline"],
                "body": item["body"],
                "published_at": item["published_at"],
                "source_portal": item["source_portal"],
                "scraped_at": datetime.now(),
            },
        )


class DailyPricePipeline:

    async def process_item(self, item, spider):
        if spider.name != "sharesansar_prices":
            return item

        await self.save_price(item)
        return item

    @sync_to_async
    def save_price(self, item):
        from companies.models import Company, DailyPrice

        try:
            company = Company.objects.get(
                symbol=item["symbol"]
            )
        except Company.DoesNotExist:
            return

        DailyPrice.objects.get_or_create(
            company=company,
            date=item["date"],
            defaults={
                "open": item["open"],
                "high": item["high"],
                "low": item["low"],
                "close": item["close"],
                "volume": item["volume"],
                "turnover": item["turnover"],
            },
        )