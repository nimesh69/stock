# ShareSansar News Spider

## Overview

`ShareSansarNewsSpider` is a Scrapy spider designed to collect the latest news articles from the ShareSansar website. It starts from the ShareSansar **Latest News** category, identifies news articles within a configurable date range, follows each article URL, and extracts the headline, article body, publication date, source URL, and source portal.

The spider is configured to respect `robots.txt`, use a two-second download delay, and identify itself with the `StockAppAssignmentCrawler/1.0` user agent.

## Spider Configuration

- **Spider name:** `sharesansar_news`
- **Start URL:** `https://www.sharesansar.com/category/latest`
- **Framework:** Scrapy
- **Robots.txt:** Enabled
- **Download delay:** 2 seconds
- **User-Agent:** `StockAppAssignmentCrawler/1.0`

## Configurable Date Range

The spider accepts a `days_back` argument when initialized. This controls how far back the crawler should retrieve news articles.

For example:

```bash
scrapy crawl sharesansar_news -a days_back=7
```

This allows the crawler to dynamically determine whether an article falls within the requested period.

## News Listing Extraction

The `parse()` method processes articles from the ShareSansar latest-news page. For each article, it extracts:

- Article URL
- Headline
- Publication date

Articles without a valid URL are ignored. The publication date is parsed before the article is processed.

## Pagination and Date Filtering

The crawler compares each article's publication date with the configured `days_back` period. Once articles fall outside the requested date range, pagination is stopped, preventing unnecessary requests for older pages.

If the current page still contains relevant articles, the spider follows the `next` pagination link and continues processing additional pages.

## Article Content Extraction

The `parse_article()` method extracts the article content from the ShareSansar news detail page.

All paragraph text under `#newsdetail-content` is collected, cleaned, and combined into a single body string. The headline is taken from the metadata passed from the listing page, with the article's `<h1>` used as a fallback.

## Output Schema

Each successfully processed article produces the following item:

| Field | Description |
|---|---|
| `headline` | News article headline |
| `body` | Full cleaned article text |
| `published_at` | Parsed publication datetime |
| `url` | Article URL |
| `source_portal` | Source identifier, set to `sharesansar` |

The final item structure is defined in `parse_article()`.

## Date Parsing

The `_parse_date()` helper converts ShareSansar's date format into a Python `datetime` object using the format:

`%A, %B %d, %Y`

If the date is missing or cannot be parsed, the method returns `None`.

## Purpose

This spider is suitable for building a news dataset for a stock-market application, including:

- Recent ShareSansar news collection
- Historical news ingestion
- News feeds
- Financial-news analysis
- Search and indexing
- Market-news monitoring