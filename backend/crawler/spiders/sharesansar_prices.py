import scrapy
from datetime import datetime, timedelta

from companies.models import Company


class ShareSansarPricesSpider(scrapy.Spider):
    name = "sharesansar_prices"
    start_urls = [
        "https://www.sharesansar.com/today-share-price"
    ]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,
        "USER_AGENT": "StockAppAssignmentCrawler/1.0",
    }

    DAYS_BACK = 1

    def parse(self, response):
        self.watchlist_symbols = set(
            Company.objects.values_list("symbol", flat=True)
        )

        today = response.css("input#fromdate::attr(value)").get()

        yield from self.extract_rows(response, today)

        for i in range(1, self.DAYS_BACK):
            target_date = (
                datetime.now() - timedelta(days=i)
            ).strftime("%Y-%m-%d")

            yield scrapy.FormRequest.from_response(
                response,
                formid="frm_todayshareprice",
                formdata={
                    "date": target_date,
                    "sector": "all_sec",
                },
                callback=self.parse_historical,
                cb_kwargs={"date": target_date},
                dont_filter=True,
            )

    def parse_historical(self, response, date):
        yield from self.extract_rows(response, date)

    def extract_rows(self, response, date):
        for row in response.css("table tbody tr"):
            cells = row.css("td")

            if len(cells) < 14:
                continue

            symbol = cells[1].css("a::text").get()

            if not symbol:
                continue

            symbol = symbol.strip()

            if symbol not in self.watchlist_symbols:
                continue

            def clean(idx):
                raw = cells[idx].css("::text").get() or "0"
                return raw.strip().replace(",", "")

            yield {
                "symbol": symbol,
                "date": date,
                "open": clean(3),
                "high": clean(4),
                "low": clean(5),
                "close": clean(6),
                "volume": clean(11),
                "turnover": clean(13),
            }