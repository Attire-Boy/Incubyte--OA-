/** One function per backend endpoint, so components never build URLs. */
import { apiRequest } from './client';

export const authApi = {
  register: (data) => apiRequest('/api/auth/register', { method: 'POST', body: data }),
  login: (data) => apiRequest('/api/auth/login', { method: 'POST', body: data }),
  me: () => apiRequest('/api/auth/me'),
};

export const vehiclesApi = {
  list: () => apiRequest('/api/vehicles'),
  search: (params) => apiRequest('/api/vehicles/search', { query: params }),
  create: (data) => apiRequest('/api/vehicles', { method: 'POST', body: data }),
  update: (id, data) => apiRequest(`/api/vehicles/${id}`, { method: 'PUT', body: data }),
  remove: (id) => apiRequest(`/api/vehicles/${id}`, { method: 'DELETE' }),
  purchase: (id, quantity = 1) =>
    apiRequest(`/api/vehicles/${id}/purchase`, { method: 'POST', body: { quantity } }),
  restock: (id, quantity) =>
    apiRequest(`/api/vehicles/${id}/restock`, { method: 'POST', body: { quantity } }),
};
