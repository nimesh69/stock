import scrapy
from datetime import datetime, timedelta

from crawler.models import CrawlRun
from django.utils import timezone
from asgiref.sync import sync_to_async

class ShareSansarNewsSpider(scrapy.Spider):
    name = "sharesansar_news"

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,
        "USER_AGENT": "StockAppAssignmentCrawler/1.0",
    }

    start_urls = [
        "https://www.sharesansar.com/category/latest"
    ]

    def __init__(self, days_back=1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.days_back = int(days_back)

        # Create crawl record when spider starts
        self.crawl_run = CrawlRun.objects.create(
            source="sharesansar_news",
            status="pending",
            started_at=timezone.now(),
        )

    def parse(self, response):
        stop_paginating = False

        for article in response.css("div.featured-news-list"):
            url = article.css(
                "div.col-md-10 a::attr(href)"
            ).get()

            title = article.css(
                "h4.featured-news-title::text"
            ).get()

            date_str = article.css(
                "p span.text-org::text"
            ).get()

            if not url:
                continue

            published_at = self._parse_date(date_str)

            if (
                published_at
                and datetime.now() - published_at
                > timedelta(days=self.days_back)
            ):
                stop_paginating = True
                continue

            yield response.follow(
                url,
                callback=self.parse_article,
                meta={
                    "headline": title.strip() if title else None,
                    "published_at": published_at,
                    "url": url,
                },
            )

        if not stop_paginating:
            next_page = response.css(
                "ul.pagination li a.page-link[rel='next']::attr(href)"
            ).get()

            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse,
                )

    def parse_article(self, response):
        paragraphs = (
            response
            .css("#newsdetail-content p")
            .xpath(".//text()")
            .getall()
        )

        body = " ".join(
            p.strip()
            for p in paragraphs
            if p.strip()
        )

        headline = (
            response.meta.get("headline")
            or response.css("h1::text").get()
            or ""
        ).strip()

        yield {
            "headline": headline,
            "body": body,
            "published_at": response.meta.get("published_at"),
            "url": response.meta.get("url") or response.url,
            "source_portal": "sharesansar",
        }

    async def closed(self, reason):
        from django.db import connection

        def _persist():
            stats = self.crawler.stats.get_stats()
            connection.close_if_unusable_or_obsolete()
            self.crawl_run.status = "success" if reason == "finished" else "failed"
            self.crawl_run.finished_at = timezone.now()
            self.crawl_run.stats = {
                "close_reason": reason,
                "items_scraped": stats.get("item_scraped_count", 0),
                "requests": stats.get("downloader/request_count", 0),
                "responses": stats.get("downloader/response_count", 0),
                "errors": stats.get("spider_exceptions", 0),
            }
            self.crawl_run.save()

        try:
            await sync_to_async(_persist, thread_sensitive=True)()
        except Exception:
            self.logger.exception("Failed to persist CrawlRun on close")

    @staticmethod
    def _parse_date(date_str):
        if not date_str:
            return None

        try:
            return datetime.strptime(
                date_str.strip(),
                "%A, %B %d, %Y",
            )
        except ValueError:
            return None