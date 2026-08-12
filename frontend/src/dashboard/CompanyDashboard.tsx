import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getBehaviorSummary } from "../api/analysis";
import { getCompanies, getCompanyPrices } from "../api/company.api";
import { getCompanyArticles } from "../api/news.api";
import type { BehaviorSummaryItem } from "../types/analysis.types";
import type { Company, DailyPrice, PriceRange } from "../types/company.types";
import type { ArticleListItem } from "../types/news.types";
import NewsListPanel from "./components/NewsListPanel";
import PageShell from "./components/PageShell";
import { ErrorLine, LoadingLine } from "./components/StatusLine";
import type { DashboardProps, LoadState } from "./types";
import { formatDate, formatNumber, getNextPage } from "./utils";

const ranges: PriceRange[] = ["1d", "7d", "30d", "90d", "1y", "all"];

export default function CompanyDashboard({ user, onLogout }: DashboardProps) {
  const { id = "" } = useParams();
  const [range, setRange] = useState<PriceRange>("30d");
  const [companies, setCompanies] = useState<Company[]>([]);
  const [prices, setPrices] = useState<DailyPrice[]>([]);
  const [behavior, setBehavior] = useState<BehaviorSummaryItem[]>([]);
  const [articles, setArticles] = useState<ArticleListItem[]>([]);
  const [pricesNext, setPricesNext] = useState<string | null>(null);
  const [behaviorNext, setBehaviorNext] = useState<string | null>(null);
  const [articlesNext, setArticlesNext] = useState<string | null>(null);
  const [state, setState] = useState<LoadState>("loading");

  const company = useMemo(
    () => companies.find((item) => String(item.id) === id),
    [companies, id],
  );

  useEffect(() => {
    const load = async () => {
      setState("loading");
      try {
        const [companyData, priceData, behaviorData, articleData] =
          await Promise.all([
            getCompanies(),
            getCompanyPrices(id, { range }),
            getBehaviorSummary(id, { range }),
            getCompanyArticles(id),
          ]);
        setCompanies(companyData.results);
        setPrices(priceData.results);
        setPricesNext(priceData.next ?? null);
        setBehavior(behaviorData.results);
        setBehaviorNext(behaviorData.next);
        setArticles(articleData.results);
        setArticlesNext(articleData.next);
        setState("idle");
      } catch {
        setState("error");
      }
    };

    load();
  }, [id, range]);

  const latestPrice = prices[0];

  const loadMorePrices = async () => {
    const page = getNextPage(pricesNext);
    if (!page) return;
    const data = await getCompanyPrices(id, { range, page });
    setPrices((current) => [...current, ...data.results]);
    setPricesNext(data.next ?? null);
  };

  const loadMoreBehavior = async () => {
    const page = getNextPage(behaviorNext);
    if (!page) return;
    const data = await getBehaviorSummary(id, { range, page });
    setBehavior((current) => [...current, ...data.results]);
    setBehaviorNext(data.next);
  };

  const loadMoreArticles = async () => {
    const page = getNextPage(articlesNext);
    if (!page) return;
    const data = await getCompanyArticles(id, page);
    setArticles((current) => [...current, ...data.results]);
    setArticlesNext(data.next);
  };

  return (
    <PageShell user={user} onLogout={onLogout}>
      <Link className="back-link" to="/dashboard">
        Back to dashboard
      </Link>
      <section className="dashboard-intro compact">
        <p className="auth-kicker">{company?.sector ?? "Company"}</p>
        <h1>
          {company ? `${company.symbol} · ${company.name}` : `Company ${id}`}
        </h1>
      </section>

      <div className="range-tabs" aria-label="Price range">
        {ranges.map((item) => (
          <button
            className={item === range ? "active" : ""}
            key={item}
            onClick={() => setRange(item)}
            type="button"
          >
            {item}
          </button>
        ))}
      </div>

      {state === "error" ? (
        <ErrorLine label="Could not load company data." />
      ) : null}
      {state === "loading" ? <LoadingLine /> : null}

      <section className="stat-grid">
        <div>
          <span>Close</span>
          <strong>{latestPrice ? formatNumber(latestPrice.close) : "-"}</strong>
        </div>
        <div>
          <span>Volume</span>
          <strong>{latestPrice ? formatNumber(latestPrice.volume) : "-"}</strong>
        </div>
        <div>
          <span>Turnover</span>
          <strong>
            {latestPrice ? formatNumber(latestPrice.turnover) : "-"}
          </strong>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-heading">
            <h2>Prices</h2>
            <span>{prices.length} rows</span>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Open</th>
                  <th>High</th>
                  <th>Low</th>
                  <th>Close</th>
                  <th>Volume</th>
                </tr>
              </thead>
              <tbody>
                {prices.map((price) => (
                  <tr key={price.date}>
                    <td>{formatDate(price.date)}</td>
                    <td>{formatNumber(price.open)}</td>
                    <td>{formatNumber(price.high)}</td>
                    <td>{formatNumber(price.low)}</td>
                    <td>{formatNumber(price.close)}</td>
                    <td>{formatNumber(price.volume)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {pricesNext ? (
            <button
              className="plain-button"
              onClick={loadMorePrices}
              type="button"
            >
              Next prices
            </button>
          ) : null}
        </div>

        <div className="panel">
          <div className="panel-heading">
            <h2>Behavior</h2>
            <span>{behavior.length} rows</span>
          </div>
          <div className="behavior-list">
            {behavior.map((item) => (
              <div
                className="behavior-row"
                key={`${item.date}-${item.pressure_indicator}`}
              >
                <strong>{formatDate(item.date)}</strong>
                <span>{item.pressure_indicator.replace("_", " ")}</span>
                <small>
                  VWAP {formatNumber(item.vwap)} · Avg vol{" "}
                  {formatNumber(item.avg_volume_20d)}
                </small>
              </div>
            ))}
          </div>
          {behaviorNext ? (
            <button
              className="plain-button"
              onClick={loadMoreBehavior}
              type="button"
            >
              Next behavior
            </button>
          ) : null}
        </div>
      </section>

      <NewsListPanel
        articles={articles}
        hasNextPage={Boolean(articlesNext)}
        loadMoreLabel="Next company news"
        onLoadMore={loadMoreArticles}
        title="Company news"
      />
    </PageShell>
  );
}
