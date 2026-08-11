export interface ApiErrorResponse {
  detail?: string;
  [key: string]: unknown;
}

export interface CsrfTokenResponse {
  csrfToken: string;
}
