import axios from "axios";

export const URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8080";

export const httpClient = axios.create({
  baseURL: URL,
});
