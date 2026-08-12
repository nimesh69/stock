import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getArticleById } from "../api/news.api";
import type { ArticleDetail } from "../types/news.types";
import PageShell from "./components/PageShell";
import { ErrorLine, LoadingLine } from "./components/StatusLine";
import type { DashboardProps, LoadState } from "./types";
import { formatDate } from "./utils";

export default function NewsDetail({ user, onLogout }: DashboardProps) {
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
