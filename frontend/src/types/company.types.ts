export interface Company {
  id: number;
  symbol: string;
  name: string;
  sector: string;
}

export interface DailyPrice {
  date: string; // "YYYY-MM-DD"
  open: string; // DecimalField serializes as string
  high: string;
  low: string;
  close: string;
  volume: number;
  turnover: string;
}

export interface CompanyListResponse {
  results: Company[];
  count?: number;
  next?: string | null;
  previous?: string | null;
}

export interface CompanyPricesResponse {
  results: DailyPrice[];
  count?: number;
  next?: string | null;
  previous?: string | null;
}

export type PriceRange = "1d" | "7d" | "30d" | "90d" | "1y" | "all";

export interface CompanyPricesParams {
  range?: PriceRange;
  from?: string; // "YYYY-MM-DD"
  page?: number;
  to?: string; // "YYYY-MM-DD"
}
