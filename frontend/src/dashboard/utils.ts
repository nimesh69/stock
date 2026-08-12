export const formatDate = (value: string | null) => {
  if (!value) return "Not dated";
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(value));
};

export const formatNumber = (value: number | string | null | undefined) => {
  if (value === null || value === undefined || value === "") return "-";
  return new Intl.NumberFormat("en").format(Number(value));
};

export const getNextPage = (url: string | null | undefined) => {
  if (!url) return null;
  return Number(
    new URL(url, window.location.origin).searchParams.get("page") ?? "1",
  );
};
