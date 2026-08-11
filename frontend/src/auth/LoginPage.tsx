import { useState } from "react";
import { loginUser } from "../api/auth.api";
import type { User } from "../types/auth.types";
import type { ApiErrorResponse } from "../types/api.types";
import axios from "axios";

interface LoginPageProps {
  onAuthenticated: (user: User) => void;
  onShowSignup: () => void;
}

const getErrorMessage = (error: unknown) => {
  if (axios.isAxiosError<ApiErrorResponse>(error)) {
    return error.response?.data?.detail ?? "Unable to login. Please try again.";
  }

  return "Unable to login. Please try again.";
};

export default function LoginPage({ onAuthenticated, onShowSignup }: LoginPageProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const data = await loginUser({ username, password });
      onAuthenticated(data.user);
    } catch (loginError) {
      setError(getErrorMessage(loginError));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-panel" aria-labelledby="login-title">
        <p className="auth-kicker">Stock dashboard</p>
        <h1 id="login-title">Login</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Username
            <input
              autoComplete="username"
              name="username"
              onChange={(event) => setUsername(event.target.value)}
              required
              type="text"
              value={username}
            />
          </label>
          <label>
            Password
            <input
              autoComplete="current-password"
              name="password"
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </label>
          {error ? <p className="auth-error">{error}</p> : null}
          <button className="auth-submit" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Logging in..." : "Login"}
          </button>
        </form>
        <button className="auth-switch" onClick={onShowSignup} type="button">
          Create an account
        </button>
      </section>
    </main>
  );
}
