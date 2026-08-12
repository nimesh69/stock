export type PressureIndicator =
  | "accumulation"
  | "distribution"
  | "weak_rally"
  | "weak_selloff"
  | "neutral";

export interface BehaviorSummaryItem {
  date: string;
  vwap: string | null;
  close: string;
  pressure_indicator: PressureIndicator;
  is_volume_anomaly: boolean;
  avg_volume_20d: number | null;
}

export interface BehaviorSummaryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: BehaviorSummaryItem[];
}