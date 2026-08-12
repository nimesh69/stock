export interface ArticleListItem {
  id: number;
  headline: string;
  source_portal: string;
  published_at: string | null;
}

export interface ArticleDetail {
  id: number;
  headline: string;
  body: string;
  url: string;
  source_portal: string;
  published_at: string | null;
}

export interface ArticleListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ArticleListItem[];
}