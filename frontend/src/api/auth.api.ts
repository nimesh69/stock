import axiosInstance from "./axios";
import type { CsrfTokenResponse } from "../types/api.types";
import type { AuthResponse, LoginPayload, SignupPayload } from "../types/auth.types";

const ACCOUNT_BASE = "/accounts";

export const getCsrfToken = async () => {
  const response = await axiosInstance.get<CsrfTokenResponse>(`${ACCOUNT_BASE}/csrf/`);
  return response.data;
};

export const loginUser = async (payload: LoginPayload) => {
  await getCsrfToken();
  const response = await axiosInstance.post<AuthResponse>(`${ACCOUNT_BASE}/login/`, payload);
  return response.data;
};

export const signupUser = async (payload: SignupPayload) => {
  await getCsrfToken();
  const response = await axiosInstance.post<AuthResponse>(`${ACCOUNT_BASE}/signup/`, payload);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await axiosInstance.get<AuthResponse>(`${ACCOUNT_BASE}/me/`);
  return response.data;
};

export const logoutUser = async () => {
  await getCsrfToken();
  const response = await axiosInstance.post<{ detail: string }>(`${ACCOUNT_BASE}/logout/`);
  return response.data;
};
