# Progress Log — Stock Market Application Assignment

## Stack decision
Django REST Framework (not FastAPI) — chosen to reuse existing DRF/Channels/Celery/Postgres experience and get Django admin as a near-free RBAC + review UI. Documented trade-off: FastAPI would be leaner but costs setup time on auth/admin tooling Django gives for free.

## Scope decisions (for the 10-hour budget — all to be stated explicitly in the final README)
- **2 news portals → cut to 1**: sharesansar.com only (merolagani dropped — older ASP.NET WebForms site, harder to scrape reliably in the time available)
- **5 companies**, not up to 10
- **No floorsheet data** — explicitly optional per the assignment brief
- **Keyword/alias-based categorization**, not NER/embeddings/LLM — justified by full-stack strength allocation
- **4 of 5 analysis outputs** — VWAP, pressure indicator, volume anomaly, findings summary kept; news-price correlation is a cut candidate if time runs short
- **Corrections via Django admin**, not a custom React review screen
- **RBAC via `is_superuser`/`is_staff`**, not a custom User model — Admin = superuser, Analyst = staff, Viewer = plain authenticated user

## Repository layout
```
Stock/            # Django project settings
accounts/         # auth views (register/login/me) — no models, uses built-in User
companies/        # Company, DailyPrice, FloorsheetTransaction models
news/             # RawArticle, ArticleCategory, CategoryCorrection models
crawler/          # Scrapy spiders + CrawlRun model + management commands
analysis/         # BehaviorSummary, NewsPriceCorrelation models
```

## Completed

### Data models
All models defined and mapped to the schema-separation requirement (raw data / categorization / computed analysis kept in distinct tables, never recomputed per-request):
- `companies/models.py` — `Company`, `DailyPrice`, `FloorsheetTransaction` (optional/unused by design)
- `news/models.py` — `RawArticle`, `ArticleCategory` (multi-label via one row per company per article), `CategoryCorrection` (audit trail)
- `crawler/models.py` — `CrawlRun` (status, stats JSONField)
- `analysis/models.py` — `BehaviorSummary`, `NewsPriceCorrelation` (optional/stretch)

### Auth (accounts app)
- DRF Token Authentication (not JWT — documented time-budget trade-off)
- `POST /api/auth/register/` — self-registration always creates a Viewer (`is_staff=False`, `is_superuser=False`)
- `POST /api/auth/login/` — built-in `obtain_auth_token`
- `GET /api/auth/me/` — returns `{username, role}` derived from `is_superuser`/`is_staff`
- Admin/Analyst accounts created via `createsuperuser` or Django admin, not self-registration; same `/login/` endpoint works for all three roles

### Crawling
- **News spider** (`crawler/spiders/sharesansar_news.py`) — selectors confirmed against real page markup (`div.featured-news-list`, `#newsdetail-content`). Cursor-based pagination with a 35-day cutoff so it doesn't crawl the entire site archive. robots.txt confirmed fully open (`Disallow:` empty).
- **News pipeline** (`crawler/pipelines.py` → `DjangoWritePipeline`) — writes to `RawArticle` via `get_or_create(url=...)`, dedup-by-URL built in.
- **Prices spider** (`crawler/spiders/sharesansar_prices.py`) — column indices confirmed against live table markup (`open=3, high=4, low=5, close=6, volume=11, turnover=13`). Filters the site's ~337-row table down to only the seeded watchlist companies.
  - ⚠️ **Unverified**: the historical-date form submission (`FormRequest.from_response` against the CSRF-protected `frm_todayshareprice` form) has not been confirmed to actually return different data per date — the search button being `type="button"` suggests possible JS/AJAX interception. **Needs testing before being trusted for a full month of data.** Fallback plan if it doesn't work cleanly within ~20-30 min: manual CSV export of historical OHLCV, loaded via a small seed command.
- **Management commands**: `crawler/management/commands/crawl_news.py` runs the news spider via `CrawlerProcess` (no separate `scrapy.cfg` needed since it runs inside `manage.py`, which already boots Django).
- **`companies/management/commands/seed_companies.py`** — seeds the 5-company watchlist (NABIL, CHCL, NLIC, SHIVM, ICFC — chosen for sector diversity). Safe to re-run; safe to extend by adding entries to `WATCHLIST`.

## Not yet done (real gaps, tracked explicitly)
- [ ] `crawl_prices` management command (spider exists, not yet wrapped as a runnable command)
- [ ] `CrawlRun` row creation/updates wired into the management commands (status, started_at/finished_at, stats) — required by the assignment's admin API endpoints, currently 100% missing
- [ ] Celery beat schedule for recurring crawls — required by Section 1.3, not yet configured at all
- [ ] Verify prices spider actually pulls distinct historical dates (see ⚠️ above) — test before trusting
- [ ] Categorization engine (keyword/alias matching, multi-label `ArticleCategory` writer)
- [ ] Analysis engine (VWAP, pressure indicator, volume anomaly, findings summary)
- [ ] DRF viewsets/serializers + permission classes for the full API surface
- [ ] `drf-spectacular` OpenAPI docs
- [ ] Frontend (Next.js) — company detail page, cross-company table
- [ ] Docker Compose full stack
- [ ] README with all scope-cut justifications
- [ ] Half-page findings summary
- [ ] End-to-end test: confirm a full crawl actually lands correct rows in Postgres (companies seeded first, then news + prices crawls)