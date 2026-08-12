import scrapy
from datetime import datetime, timedelta


class ShareSansarNewsSpider(scrapy.Spider):
    name = "sharesansar_news"

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,
        "USER_AGENT": "StockAppAssignmentCrawler/1.0",
    }

    start_urls = ["https://www.sharesansar.com/category/latest"]

    def __init__(self, days_back=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.days_back = int(days_back)

    def parse(self, response):
        stop_paginating = False

        for article in response.css("div.featured-news-list"):
            url = article.css("div.col-md-10 a::attr(href)").get()
            title = article.css("h4.featured-news-title::text").get()
            date_str = article.css("p span.text-org::text").get()

            if not url:
                continue

            published_at = self._parse_date(date_str)

            # Replaced hardcoded MAX_AGE_DAYS with self.days_back
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
        paragraphs = response.css("#newsdetail-content p").xpath(".//text()").getall()

        body = " ".join(p.strip() for p in paragraphs if p.strip())

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