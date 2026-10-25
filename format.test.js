import { describe, it, expect } from 'vitest';
import { formatPrice, stockLabel, hasActiveFilters, toSearchParams } from './format';

describe('formatPrice', () => {
  it('formats whole dollars with separators', () => {
    expect(formatPrice(21550)).toBe('$21,550');
  });
});

describe('stockLabel', () => {
  it('describes sold out, last unit and plural stock', () => {
    expect(stockLabel(0)).toBe('Sold out');
    expect(stockLabel(1)).toBe('Last one on the lot');
    expect(stockLabel(6)).toBe('6 on the lot');
  });
});

describe('filters', () => {
  it('detects whether any server-side filter is set', () => {
    expect(hasActiveFilters({ query: '', category: '', minPrice: '', maxPrice: '' })).toBe(false);
    expect(hasActiveFilters({ query: 'rav', category: '', minPrice: '', maxPrice: '' })).toBe(true);
  });

  it('maps UI filters to API search params', () => {
    expect(
      toSearchParams({ query: ' toyota ', category: 'SUV', minPrice: '1000', maxPrice: '' }, 'make'),
    ).toEqual({ make: 'toyota', category: 'SUV', min_price: 1000 });
  });
});
