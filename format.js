export const CATEGORIES = ['Sedan', 'SUV', 'Truck', 'Coupe', 'Hatchback', 'Convertible', 'Electric', 'Van'];

const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

export const formatPrice = (value) => currency.format(value);

export function stockLabel(quantity) {
  if (quantity <= 0) return 'Sold out';
  if (quantity === 1) return 'Last one on the lot';
  return `${quantity} on the lot`;
}

export const EMPTY_FILTERS = { query: '', field: 'make', category: '', minPrice: '', maxPrice: '' };

export function hasActiveFilters({ query, category, minPrice, maxPrice }) {
  return Boolean(query.trim() || category || minPrice !== '' || maxPrice !== '');
}

/** Map the filter bar's state to /api/vehicles/search query params. */
export function toSearchParams({ query, category, minPrice, maxPrice }, field = 'make') {
  const params = {};
  if (query.trim()) params[field] = query.trim();
  if (category) params.category = category;
  if (minPrice !== '') params.min_price = Number(minPrice);
  if (maxPrice !== '') params.max_price = Number(maxPrice);
  return params;
}
