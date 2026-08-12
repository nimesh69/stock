import { Link } from "react-router-dom";
import type { ArticleListItem } from "../../types/news.types";
import type { LoadState } from "../types";
import { formatDate } from "../utils";
import { ErrorLine, LoadingLine } from "./StatusLine";

interface NewsListPanelProps {
  articles: ArticleListItem[];
  errorLabel?: string;
  hasNextPage: boolean;
  loadMoreLabel: string;
  showInitialLoading?: boolean;
  state?: LoadState;
  title: string;
  onLoadMore: () => void;
}

export default function NewsListPanel({
  articles,
  errorLabel = "Could not load news.",
  hasNextPage,
  loadMoreLabel,
  onLoadMore,
  showInitialLoading = false,
  state = "idle",
  title,
}: NewsListPanelProps) {
  return (
    <div className="panel">
      <div className="panel-heading">
        <h2>{title}</h2>
        <span>{articles.length} shown</span>
      </div>
      {state === "error" ? <ErrorLine label={errorLabel} /> : null}
      {showInitialLoading && state === "loading" && articles.length === 0 ? (
        <LoadingLine />
      ) : null}
      <div className="news-list">
        {articles.map((article) => (
          <Link className="news-row" key={article.id} to={`/news/${article.id}`}>
            <strong>{article.headline}</strong>
            <span>
              {article.source_portal} · {formatDate(article.published_at)}
            </span>
          </Link>
        ))}
      </div>
      {hasNextPage ? (
        <button className="plain-button" onClick={onLoadMore} type="button">
          {state === "loading" ? "Loading..." : loadMoreLabel}
        </button>
      ) : null}
    </div>
  );
}
