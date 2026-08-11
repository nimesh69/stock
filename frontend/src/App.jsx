import { useEffect, useState } from "react";
import { getCurrentUser, logoutUser } from "./api/auth.api";
import AppRoutes from "./routes/AppRoutes";
import "./App.css";

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [isCheckingUser, setIsCheckingUser] = useState(true);

  useEffect(() => {
    const checkUser = async () => {
      try {
        const data = await getCurrentUser();
        setCurrentUser(data.user);
      } catch {
        setCurrentUser(null);
      } finally {
        setIsCheckingUser(false);
      }
    };

    checkUser();
  }, []);

  const handleLogout = async () => {
    await logoutUser();
    setCurrentUser(null);
  };

  if (isCheckingUser) {
    return <main className="auth-page">Loading...</main>;
  }

  return (
    <AppRoutes
      currentUser={currentUser}
      onAuthenticated={setCurrentUser}
      onLogout={handleLogout}
    />
  );
}

export default App;
