import axiosInstance from "./axios";
import type { BehaviorSummaryResponse } from "../types/analysis.types";
import type { PriceRange } from "../types/company.types";

const COMPANY_BASE = "/companies";

export const getBehaviorSummary = async (
  companyId: number | string,
  params?: { range?: PriceRange; from?: string; to?: string }
) => {
  const response = await axiosInstance.get<BehaviorSummaryResponse>(
    `${COMPANY_BASE}/${companyId}/behavior-summary`,
    { params }
  );
  return response.data;
};