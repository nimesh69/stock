import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import LoginPage from "../auth/LoginPage";
import SignupPage from "../auth/SignupPage";
import CompanyDashboard from "../dashboard/CompanyDashboard";
import Dashboard from "../dashboard/DashboardPage";
import NewsDetail from "../dashboard/NewsDetail";
import type { User } from "../types/auth.types";

interface AppRoutesProps {
  currentUser: User | null;
  onAuthenticated: (user: User) => void;
  onLogout: () => void;
}

function LoginRoute({ currentUser, onAuthenticated }: { currentUser: User | null; onAuthenticated: (user: User) => void; }) {
  const navigate = useNavigate();

  if (currentUser) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <LoginPage
      onAuthenticated={(user) => {
        onAuthenticated(user);
        navigate("/dashboard");
      }}
      onShowSignup={() => navigate("/signup")}
    />
  );
}

function SignupRoute({ currentUser, onAuthenticated }: { currentUser: User | null; onAuthenticated: (user: User) => void; }) {
  const navigate = useNavigate();

  if (currentUser) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <SignupPage
      onAuthenticated={(user) => {
        onAuthenticated(user);
        navigate("/dashboard");
      }}
      onShowLogin={() => navigate("/login")}
    />
  );
}

function AuthenticatedRoute({ currentUser, children }: { currentUser: User | null; children: JSX.Element; }) {
  return currentUser ? children : <Navigate to="/login" replace />;
}

export default function AppRoutes({ currentUser, onAuthenticated, onLogout }: AppRoutesProps) {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={<LoginRoute currentUser={currentUser} onAuthenticated={onAuthenticated} />}
        />
        <Route
          path="/signup"
          element={<SignupRoute currentUser={currentUser} onAuthenticated={onAuthenticated} />}
        />
        <Route
          path="/dashboard"
          element={
            <AuthenticatedRoute currentUser={currentUser}>
              <Dashboard user={currentUser!} onLogout={onLogout} />
            </AuthenticatedRoute>
          }
        />
        <Route
          path="/companies/:id"
          element={
            <AuthenticatedRoute currentUser={currentUser}>
              <CompanyDashboard user={currentUser!} onLogout={onLogout} />
            </AuthenticatedRoute>
          }
        />
        <Route
          path="/news/:id"
          element={
            <AuthenticatedRoute currentUser={currentUser}>
              <NewsDetail user={currentUser!} onLogout={onLogout} />
            </AuthenticatedRoute>
          }
        />
        <Route
          path="/*"
          element={
            <Navigate to={currentUser ? "/dashboard" : "/login"} replace />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
