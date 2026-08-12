import { Link } from "react-router-dom";
import type { ReactNode } from "react";
import type { DashboardProps } from "../types";

interface PageShellProps extends DashboardProps {
  children: ReactNode;
}

export default function PageShell({ children, onLogout, user }: PageShellProps) {
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
