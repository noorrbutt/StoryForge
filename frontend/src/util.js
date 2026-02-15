export const API_BASE_URL = import.meta.env.PROD
  ? "/api" // Production: relative URL (Vercel routes to backend)
  : "http://localhost:8000/api"; // Development: local backend
