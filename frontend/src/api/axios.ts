import axios from "axios";
// import.meta.env
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
});

// ─── Request interceptor ───────────────────────────────────────────────────
axiosInstance.interceptors.request.use(
  (config) => {
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }

    // Keep your FormData logging if needed
    // let dataToLog = config.data;
    // if (config.data instanceof FormData) { ... }

    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  },
);

// ─── Response interceptor ──────────────────────────────────────────────────
interface QueueItem {
  resolve: (value?: unknown) => void;
  reject: (error: unknown) => void;
}
let isRefreshing = false;
let failedQueue: QueueItem[] = [];

const processQueue = (error: unknown) => {
  failedQueue.forEach(({ resolve, reject }) =>
    error ? reject(error) : resolve(),
  );
  failedQueue = [];
};
export default axiosInstance;
