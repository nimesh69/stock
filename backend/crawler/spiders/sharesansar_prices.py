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

    DAYS_BACK = 10

    @sync_to_async
    def get_watchlist_symbols(self):
        return set(
            Company.objects.values_list("symbol", flat=True)
        )

    async def parse(self, response):
        self.watchlist_symbols = await self.get_watchlist_symbols()
        self.csrf_token = response.css('input[name="_token"]::attr(value)').get()
        today = response.css("input#fromdate::attr(value)").get()

        # Today's data
        for item in self.extract_rows(response, today):
            yield item

        # Historical data — FIXED INDENTATION
        for i in range(1, self.DAYS_BACK + 1):
            target_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            self.logger.info("Requesting historical prices for %s", target_date)

            yield scrapy.FormRequest(  # ← THIS MUST BE INDENTED INSIDE THE for LOOP
                url="https://www.sharesansar.com/ajaxtodayshareprice",
                method="POST",
                formdata={
                    "_token": self.csrf_token,
                    "date": target_date,
                    "sector": "all_sec",
                },
                headers={
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "https://www.sharesansar.com/today-share-price",
                },
                callback=self.parse_historical,
                cb_kwargs={"date": target_date},
                dont_filter=True,
            )

    def parse_historical(self, response, date):
        self.logger.info(
            "Historical response: date=%s status=%s length=%s",
            date, response.status, len(response.text),
        )
    
        # Check if response actually contains table data
        if "headFixed" not in response.text or "<tbody>" not in response.text:
            self.logger.warning("No valid table data for %s", date)
            return
    
        selector = scrapy.Selector(text=response.text, type="html")
        
        # Debug: count rows
        rows = selector.css("table tbody tr")
        self.logger.info("Total rows found for %s: %d", date, len(rows))
        
        for item in self.extract_rows(selector, date):
            yield item


    def extract_rows(self, selector, date):
        rows = selector.css("table tbody tr")
        self.logger.info("Total rows found for %s: %d", date, len(rows))

        for row in rows:
            cells = row.css("td")

            if len(cells) < 14:
                self.logger.debug("Skipping row with only %d cells", len(cells))
                continue

            # Try multiple ways to get symbol
            symbol = cells[1].css("a::text").get()
            if not symbol:
                symbol = cells[1].css("::text").get()

            if not symbol:
                self.logger.debug("No symbol in row, cells[1] HTML: %s", cells[1].get())
                continue

            symbol = symbol.strip()

            # DEBUG: log every symbol found vs watchlist
            if symbol not in self.watchlist_symbols:
                self.logger.debug("Symbol %s not in watchlist", symbol)
                continue
            
            self.logger.info("Processing symbol: %s for date: %s", symbol, date)

            def clean(idx):
                raw = cells[idx].css("::text").get() or "0"
                return raw.strip().replace(",", "")

            def decimal(idx):
                value = clean(idx)
                try:
                    return Decimal(value)
                except InvalidOperation:
                    self.logger.warning("Invalid decimal for %s at idx %d: %r", symbol, idx, value)
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