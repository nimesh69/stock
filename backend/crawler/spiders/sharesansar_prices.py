import scrapy
from datetime import datetime, timedelta

from asgiref.sync import sync_to_async
from companies.models import Company
from decimal import Decimal, InvalidOperation

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

    DAYS_BACK = 30

    @sync_to_async
    def get_watchlist_symbols(self):
        return set(
            Company.objects.values_list("symbol", flat=True)
        )

    async def parse(self, response):
        self.watchlist_symbols = await self.get_watchlist_symbols()

        today = response.css(
            "input#fromdate::attr(value)"
        ).get()

        for item in self.extract_rows(response, today):
            yield item

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
        for item in self.extract_rows(response, date):
            yield item

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

            def decimal(idx):
                value = clean(idx)

                try:
                    return Decimal(value)
                except InvalidOperation:
                    return Decimal("0")

            def integer(idx):
                value = clean(idx)

                try:
                    return int(Decimal(value))
                except (ValueError, InvalidOperation):
                    return 0

            yield {
                "symbol": symbol,
                "date": date,
                "open": decimal(3),
                "high": decimal(4),
                "low": decimal(5),
                "close": decimal(6),
                "volume": integer(11),
                "turnover": decimal(13),
            }
