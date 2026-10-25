/**
 * Thin fetch wrapper: JSON in/out, bearer token, and readable errors.
 * In dev, Vite proxies /api to the backend; in production set VITE_API_URL.
 */

const API_BASE = import.meta.env.VITE_API_URL ?? '';
const TOKEN_KEY = 'lotline.token';

export const tokenStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
};

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

/** Turn FastAPI's `detail` (string or validation list) into one sentence. */
function describeError(detail, status) {
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail) && detail.length) {
    return detail
      .map(({ loc = [], msg }) => {
        const field = loc.filter((part) => part !== 'body' && part !== 'query').join('.');
        return field ? `${field}: ${msg}` : msg;
      })
      .join('; ');
  }
  return `Request failed (${status})`;
}

function buildUrl(path, query) {
  if (!query) return `${API_BASE}${path}`;
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') params.append(key, String(value));
  });
  const qs = params.toString();
  return `${API_BASE}${path}${qs ? `?${qs}` : ''}`;
}

export async function apiRequest(path, { method = 'GET', body, query } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  const token = tokenStore.get();
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(buildUrl(path, query), {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(response.status, describeError(data?.detail, response.status));
  return data;
}
