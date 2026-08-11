import { useState } from "react";
import axios from "axios";
import { signupUser } from "../api/auth.api";
import type { User } from "../types/auth.types";
import type { ApiErrorResponse } from "../types/api.types";

interface SignupPageProps {
  onAuthenticated: (user: User) => void;
  onShowLogin: () => void;
}

const getErrorMessage = (error: unknown) => {
  if (axios.isAxiosError<ApiErrorResponse>(error)) {
    return error.response?.data?.detail ?? "Unable to create account. Please try again.";
  }

  return "Unable to create account. Please try again.";
};

export default function SignupPage({ onAuthenticated, onShowLogin }: SignupPageProps) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const data = await signupUser({ username, email, password });
      onAuthenticated(data.user);
    } catch (signupError) {
      setError(getErrorMessage(signupError));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-panel" aria-labelledby="signup-title">
        <p className="auth-kicker">Stock dashboard</p>
        <h1 id="signup-title">Sign up</h1>
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
            Email
            <input
              autoComplete="email"
              name="email"
              onChange={(event) => setEmail(event.target.value)}
              type="email"
              value={email}
            />
          </label>
          <label>
            Password
            <input
              autoComplete="new-password"
              name="password"
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </label>
          {error ? <p className="auth-error">{error}</p> : null}
          <button className="auth-submit" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Creating account..." : "Sign up"}
          </button>
        </form>
        <button className="auth-switch" onClick={onShowLogin} type="button">
          Back to login
        </button>
      </section>
    </main>
  );
}
