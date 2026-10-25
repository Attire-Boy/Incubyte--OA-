import { CATEGORIES, EMPTY_FILTERS, hasActiveFilters } from '../utils/format';

/** Search and filter controls. Pure presentational: state lives in the page. */
export default function FilterBar({ filters, onChange, inStockOnly, onInStockOnlyChange }) {
  const set = (key) => (event) => onChange({ ...filters, [key]: event.target.value });
  const active = hasActiveFilters(filters) || inStockOnly;

  return (
    <section aria-label="Search and filter vehicles" className="rounded-md border border-concrete-deep bg-paper p-4">
      <div className="grid gap-3 md:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_minmax(0,1.3fr)]">
        <div>
          <label htmlFor="filter-query" className="field-label">
            Search by
          </label>
          <div className="flex">
            <select
              aria-label="Search field"
              value={filters.field}
              onChange={set('field')}
              className="field w-auto rounded-r-none border-r-0 bg-concrete font-semibold"
            >
              <option value="make">Make</option>
              <option value="model">Model</option>
            </select>
            <input
              id="filter-query"
              type="search"
              className="field rounded-l-none"
              placeholder={filters.field === 'make' ? 'Toyota, Ford, Tata…' : 'Corolla, F-150, Nexon…'}
              value={filters.query}
              onChange={set('query')}
            />
          </div>
        </div>

        <div>
          <label htmlFor="filter-category" className="field-label">
            Category
          </label>
          <select id="filter-category" className="field" value={filters.category} onChange={set('category')}>
            <option value="">All categories</option>
            {CATEGORIES.map((category) => (
              <option key={category}>{category}</option>
            ))}
          </select>
        </div>

        <fieldset>
          <legend className="field-label">Price range (USD)</legend>
          <div className="flex items-center gap-2">
            <input
              aria-label="Minimum price"
              type="number"
              min="0"
              inputMode="numeric"
              className="field"
              placeholder="Min"
              value={filters.minPrice}
              onChange={set('minPrice')}
            />
            <span aria-hidden="true" className="text-mute">to</span>
            <input
              aria-label="Maximum price"
              type="number"
              min="0"
              inputMode="numeric"
              className="field"
              placeholder="Max"
              value={filters.maxPrice}
              onChange={set('maxPrice')}
            />
          </div>
        </fieldset>
      </div>

      <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
        <label className="flex cursor-pointer items-center gap-2 text-sm font-medium">
          <input
            type="checkbox"
            className="size-4 accent-asphalt"
            checked={inStockOnly}
            onChange={(event) => onInStockOnlyChange(event.target.checked)}
          />
          Only show vehicles in stock
        </label>
        {active && (
          <button
            type="button"
            className="text-sm font-semibold text-steel underline-offset-4 hover:underline"
            onClick={() => {
              onChange(EMPTY_FILTERS);
              onInStockOnlyChange(false);
            }}
          >
            Clear filters
          </button>
        )}
      </div>
    </section>
  );
}
