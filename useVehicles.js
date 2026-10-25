import { useCallback, useEffect, useRef, useState } from 'react';
import { vehiclesApi } from '../api/endpoints';
import { hasActiveFilters, toSearchParams } from '../utils/format';

const DEBOUNCE_MS = 300;

/**
 * Loads vehicles for the current filters (debounced) and exposes
 * helpers to patch the local list after a mutation.
 */
export function useVehicles(filters) {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const requestId = useRef(0);

  const load = useCallback(async (currentFilters) => {
    const id = ++requestId.current;
    setLoading(true);
    try {
      const data = hasActiveFilters(currentFilters)
        ? await vehiclesApi.search(toSearchParams(currentFilters, currentFilters.field))
        : await vehiclesApi.list();
      if (id === requestId.current) {
        setVehicles(data);
        setError('');
      }
    } catch (err) {
      if (id === requestId.current) setError(err.message);
    } finally {
      if (id === requestId.current) setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => load(filters), DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [filters, load]);

  const replace = useCallback(
    (updated) => setVehicles((list) => list.map((v) => (v.id === updated.id ? updated : v))),
    [],
  );
  const remove = useCallback((id) => setVehicles((list) => list.filter((v) => v.id !== id)), []);
  const reload = useCallback(() => load(filters), [filters, load]);

  return { vehicles, loading, error, replace, remove, reload };
}
