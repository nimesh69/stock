import { Link } from "react-router-dom";
import type { Company } from "../../types/company.types";
import type { LoadState } from "../types";
import { ErrorLine, LoadingLine } from "./StatusLine";

interface CompanyListPanelProps {
  companies: Company[];
  hasNextPage: boolean;
  state: LoadState;
  onLoadMore: () => void;
}

export default function CompanyListPanel({
  companies,
  hasNextPage,
  onLoadMore,
  state,
}: CompanyListPanelProps) {
  return (
    <div className="panel">
      <div className="panel-heading">
        <h2>Companies</h2>
        <span>{companies.length} shown</span>
      </div>
      {state === "error" ? <ErrorLine label="Could not load companies." /> : null}
      {state === "loading" && companies.length === 0 ? <LoadingLine /> : null}
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
      {hasNextPage ? (
        <button className="plain-button" onClick={onLoadMore} type="button">
          {state === "loading" ? "Loading..." : "Next companies"}
        </button>
      ) : null}
    </div>
  );
}
