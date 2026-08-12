import type { User } from "../types/auth.types";

export interface DashboardProps {
  user: User;
  onLogout: () => void;
}

export type LoadState = "idle" | "loading" | "error";
