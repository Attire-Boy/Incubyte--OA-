import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiRequest, ApiError, tokenStore } from './client';

function mockFetch(status, body) {
  const response = {
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body),
  };
  global.fetch = vi.fn().mockResolvedValue(response);
  return global.fetch;
}

describe('apiRequest', () => {
  beforeEach(() => tokenStore.clear());

  it('sends JSON and returns the parsed body', async () => {
    const fetch = mockFetch(200, { ok: true });
    const result = await apiRequest('/api/things', { method: 'POST', body: { a: 1 } });
    expect(result).toEqual({ ok: true });
    const [url, init] = fetch.mock.calls[0];
    expect(url).toBe('/api/things');
    expect(init.body).toBe(JSON.stringify({ a: 1 }));
    expect(init.headers['Content-Type']).toBe('application/json');
  });

  it('attaches the bearer token when one is stored', async () => {
    tokenStore.set('abc123');
    const fetch = mockFetch(200, []);
    await apiRequest('/api/vehicles');
    expect(fetch.mock.calls[0][1].headers.Authorization).toBe('Bearer abc123');
  });

  it('omits Authorization when there is no token', async () => {
    const fetch = mockFetch(200, []);
    await apiRequest('/api/vehicles');
    expect(fetch.mock.calls[0][1].headers.Authorization).toBeUndefined();
  });

  it('returns null for 204 No Content', async () => {
    mockFetch(204, undefined);
    expect(await apiRequest('/api/vehicles/1', { method: 'DELETE' })).toBeNull();
  });

  it('throws ApiError with the server detail on failure', async () => {
    mockFetch(409, { detail: 'Only 0 unit(s) in stock' });
    const error = await apiRequest('/api/x').catch((e) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect(error.status).toBe(409);
    expect(error.message).toBe('Only 0 unit(s) in stock');
  });

  it('flattens FastAPI validation errors into a readable message', async () => {
    mockFetch(422, { detail: [{ loc: ['body', 'price'], msg: 'Input should be greater than 0' }] });
    const error = await apiRequest('/api/x').catch((e) => e);
    expect(error.message).toBe('price: Input should be greater than 0');
  });

  it('builds query strings and skips empty params', async () => {
    const fetch = mockFetch(200, []);
    await apiRequest('/api/vehicles/search', { query: { make: 'Toyota', model: '', min_price: 0 } });
    expect(fetch.mock.calls[0][0]).toBe('/api/vehicles/search?make=Toyota&min_price=0');
  });
});
