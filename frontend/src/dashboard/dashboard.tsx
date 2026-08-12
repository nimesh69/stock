import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getBehaviorSummary } from "../api/analysis";
import { getCompanies, getCompanyPrices } from "../api/company.api";
import {
  getArticleById,
  getArticles,
  getCompanyArticles,
} from "../api/news.api";
import type { BehaviorSummaryItem } from "../types/analysis.types";
import type { Company, DailyPrice, PriceRange } from "../types/company.types";
import type { ArticleDetail, ArticleListItem } from "../types/news.types";
import type { User } from "../types/auth.types";

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

type LoadState = "idle" | "loading" | "error";

const ranges: PriceRange[] = ["1d", "7d", "30d", "90d", "1y", "all"];

const formatDate = (value: string | null) => {
  if (!value) return "Not dated";
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(value));
};

const formatNumber = (value: number | string | null | undefined) => {
  if (value === null || value === undefined || value === "") return "-";
  return new Intl.NumberFormat("en").format(Number(value));
};

const getNextPage = (url: string | null | undefined) => {
  if (!url) return null;
  return Number(
    new URL(url, window.location.origin).searchParams.get("page") ?? "1",
  );
};

function PageShell({
  children,
  onLogout,
  user,
}: DashboardProps & { children: React.ReactNode }) {
  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <Link className="brand-link" to="/dashboard">
          Market Insight
        </Link>
        <div className="header-actions">
          <span>{user.username}</span>
          <button className="ghost-button" onClick={onLogout} type="button">
            Logout
          </button>
        </div>
      </header>
      {children}
    </main>
  );
}

function LoadingLine({ label = "Loading..." }: { label?: string }) {
  return <p className="muted">{label}</p>;
}

function ErrorLine({ label }: { label: string }) {
  return <p className="auth-error">{label}</p>;
}

export default function Dashboard({ user, onLogout }: DashboardProps) {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [articles, setArticles] = useState<ArticleListItem[]>([]);
  const [companyNext, setCompanyNext] = useState<string | null>(null);
  const [articleNext, setArticleNext] = useState<string | null>(null);
  const [companyState, setCompanyState] = useState<LoadState>("loading");
  const [articleState, setArticleState] = useState<LoadState>("loading");

  useEffect(() => {
    const loadCompanies = async () => {
      try {
        const data = await getCompanies();
        setCompanies(data.results);
        setCompanyNext(data.next ?? null);
        setCompanyState("idle");
      } catch {
        setCompanyState("error");
      }
    };

    const loadArticles = async () => {
      try {
        const data = await getArticles();
        setArticles(data.results);
        setArticleNext(data.next);
        setArticleState("idle");
      } catch {
        setArticleState("error");
      }
    };

    loadCompanies();
    loadArticles();
  }, []);

  const loadMoreCompanies = async () => {
    const page = getNextPage(companyNext);
    if (!page) return;
    setCompanyState("loading");
    try {
      const data = await getCompanies(page);
      setCompanies((current) => [...current, ...data.results]);
      setCompanyNext(data.next ?? null);
      setCompanyState("idle");
    } catch {
      setCompanyState("error");
    }
  };

  const loadMoreArticles = async () => {
    const page = getNextPage(articleNext);
    if (!page) return;
    setArticleState("loading");
    try {
      const data = await getArticles(page);
      setArticles((current) => [...current, ...data.results]);
      setArticleNext(data.next);
      setArticleState("idle");
    } catch {
      setArticleState("error");
    }
  };

  return (
    <PageShell user={user} onLogout={onLogout}>
      <section className="dashboard-intro">
        <p className="auth-kicker">Overview</p>
        <h1>Simple market dashboard</h1>
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-heading">
            <h2>Companies</h2>
            <span>{companies.length} shown</span>
          </div>
          {companyState === "error" ? (
            <ErrorLine label="Could not load companies." />
          ) : null}
          {companyState === "loading" && companies.length === 0 ? (
            <LoadingLine />
          ) : null}
          <div className="company-list">
            {companies.map((company) => (
              <Link
                className="list-row"
                key={company.id}
                to={`/companies/${company.id}`}
              >
                <strong>{company.symbol}</strong>
                <span>{company.name}</span>
                <small>{company.sector}</small>
              </Link>
            ))}
          </div>
          {companyNext ? (
            <button
              className="plain-button"
              onClick={loadMoreCompanies}
              type="button"
            >
              {companyState === "loading" ? "Loading..." : "Next companies"}
            </button>
          ) : null}
        </div>

        <div className="panel">
          <div className="panel-heading">
            <h2>Latest news</h2>
            <span>{articles.length} shown</span>
          </div>
          {articleState === "error" ? (
            <ErrorLine label="Could not load news." />
          ) : null}
          {articleState === "loading" && articles.length === 0 ? (
            <LoadingLine />
          ) : null}
          <div className="news-list">
            {articles.map((article) => (
              <Link
                className="news-row"
                key={article.id}
                to={`/news/${article.id}`}
              >
                <strong>{article.headline}</strong>
                <span>
                  {article.source_portal} · {formatDate(article.published_at)}
                </span>
              </Link>
            ))}
          </div>
          {articleNext ? (
            <button
              className="plain-button"
              onClick={loadMoreArticles}
              type="button"
            >
              {articleState === "loading" ? "Loading..." : "Next news"}
            </button>
          ) : null}
        </div>
      </section>
    </PageShell>
  );
}

export function CompanyDashboard({ user, onLogout }: DashboardProps) {
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
          <strong>
            {latestPrice ? formatNumber(latestPrice.volume) : "-"}
          </strong>
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

      <section className="panel">
        <div className="panel-heading">
          <h2>Company news</h2>
          <span>{articles.length} shown</span>
        </div>
        <div className="news-list">
          {articles.map((article) => (
            <Link
              className="news-row"
              key={article.id}
              to={`/news/${article.id}`}
            >
              <strong>{article.headline}</strong>
              <span>
                {article.source_portal} · {formatDate(article.published_at)}
              </span>
            </Link>
          ))}
        </div>
        {articlesNext ? (
          <button
            className="plain-button"
            onClick={loadMoreArticles}
            type="button"
          >
            Next company news
          </button>
        ) : null}
      </section>
    </PageShell>
  );
}

export function NewsDetail({ user, onLogout }: DashboardProps) {
  const { id = "" } = useParams();
  const [article, setArticle] = useState<ArticleDetail | null>(null);
  const [state, setState] = useState<LoadState>("loading");

  useEffect(() => {
    const load = async () => {
      setState("loading");
      try {
        const data = await getArticleById(id);
        setArticle(data);
        setState("idle");
      } catch {
        setState("error");
      }
    };

    load();
  }, [id]);

  return (
    <PageShell user={user} onLogout={onLogout}>
      <Link className="back-link" to="/dashboard">
        Back to dashboard
      </Link>
      {state === "loading" ? <LoadingLine /> : null}
      {state === "error" ? <ErrorLine label="Could not load article." /> : null}
      {article ? (
        <article className="article-detail">
          <p className="auth-kicker">
            {article.source_portal} · {formatDate(article.published_at)}
          </p>
          <h1>{article.headline}</h1>
          <p>{article.body}</p>
          {article.url ? (
            <a
              className="plain-button inline"
              href={article.url}
              rel="noreferrer"
              target="_blank"
            >
              Open source
            </a>
          ) : null}
        </article>
      ) : null}
    </PageShell>
  );
}
