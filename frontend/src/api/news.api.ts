import axiosInstance from "./axios";
import type { ArticleListResponse, ArticleDetail } from "../types/news.types";

const NEWS_BASE = "/news";

export const getArticles = async (page: number = 1) => {
  const response = await axiosInstance.get<ArticleListResponse>(`${NEWS_BASE}`, {
    params: { page },
  });
  return response.data;
};

export const getArticleById = async (id: number | string) => {
  const response = await axiosInstance.get<ArticleDetail>(`${NEWS_BASE}/${id}`);
  return response.data;
};