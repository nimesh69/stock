import { useEffect, useState } from "react";
import { getCompanies } from "../api/company.api";
import { getArticles } from "../api/news.api";
import type { Company } from "../types/company.types";
import type { ArticleListItem } from "../types/news.types";
import CompanyListPanel from "./components/CompanyListPanel";
import NewsListPanel from "./components/NewsListPanel";
import PageShell from "./components/PageShell";
import type { DashboardProps, LoadState } from "./types";
import { getNextPage } from "./utils";

export default function DashboardPage({ user, onLogout }: DashboardProps) {
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
        <CompanyListPanel
          companies={companies}
          hasNextPage={Boolean(companyNext)}
          onLoadMore={loadMoreCompanies}
          state={companyState}
        />
        <NewsListPanel
          articles={articles}
          hasNextPage={Boolean(articleNext)}
          loadMoreLabel="Next news"
          onLoadMore={loadMoreArticles}
          showInitialLoading
          state={articleState}
          title="Latest news"
        />
      </section>
    </PageShell>
  );
}
