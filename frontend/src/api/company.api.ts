import axiosInstance from "./axios";
import type {
  Company,
  CompanyListResponse,
  CompanyPricesResponse,
  CompanyPricesParams,
} from "../types/company.types";

const COMPANY_BASE = "/companies";

export const getCompanies = async () => {
  const response = await axiosInstance.get<CompanyListResponse>(`${COMPANY_BASE}`);
  return response.data;
};

export const getCompanyPrices = async (id: number | string, params?: CompanyPricesParams) => {
  const response = await axiosInstance.get<CompanyPricesResponse>(
    `${COMPANY_BASE}/${id}/prices`,
    { params }
  );
  return response.data;
};