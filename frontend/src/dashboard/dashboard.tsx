import type { User } from "../types/auth.types";

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

export default function Dashboard({ user, onLogout }: DashboardProps) {
  return (
    <main className="dashboard-page">
      <section className="dashboard-shell">
        <div>
          <p className="auth-kicker">Welcome</p>
          <h1>{user.username}</h1>
          <p className="dashboard-copy">You are logged in to the stock dashboard.</p>
        </div>
        <button className="auth-submit" onClick={onLogout} type="button">
          Logout
        </button>
      </section>
    </main>
  );
}
