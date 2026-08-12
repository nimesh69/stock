import axiosInstance from "./axios";
import type {
  Company,
  CompanyListResponse,
  CompanyPricesResponse,
  CompanyPricesParams,
} from "../types/company.types";

const COMPANY_BASE = "/api/companies";

export const getCompanies = async (page: number = 1) => {
  const response = await axiosInstance.get<CompanyListResponse>(`${COMPANY_BASE}`, {
    params: { page },
  });
  return response.data;
};

export const getCompanyPrices = async (id: number | string, params?: CompanyPricesParams) => {
  const response = await axiosInstance.get<CompanyPricesResponse>(
    `${COMPANY_BASE}/${id}/prices`,
    { params }
  );
  return response.data;
};
