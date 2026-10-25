import { useCallback, useMemo, useState } from 'react';
import { vehiclesApi } from '../api/endpoints';
import { ApiError } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useVehicles } from '../hooks/useVehicles';
import { EMPTY_FILTERS, hasActiveFilters } from '../utils/format';
import AppHeader from '../components/AppHeader';
import FilterBar from '../components/FilterBar';
import VehicleCard from '../components/VehicleCard';
import VehicleForm from '../components/VehicleForm';
import RestockForm from '../components/RestockForm';
import Modal from '../components/Modal';
import Toast from '../components/Toast';

export default function DashboardPage() {
  const { isAdmin, logout } = useAuth();
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [inStockOnly, setInStockOnly] = useState(false);
  const { vehicles, loading, error, replace, remove, reload } = useVehicles(filters);

  // dialog: null | { type: 'create' } | { type: 'edit'|'restock'|'delete', vehicle }
  const [dialog, setDialog] = useState(null);
  const [busyId, setBusyId] = useState(null);
  const [toast, setToast] = useState(null);
  const closeDialog = useCallback(() => setDialog(null), []);
  const dismissToast = useCallback(() => setToast(null), []);

  const visible = useMemo(
    () => (inStockOnly ? vehicles.filter((v) => v.quantity > 0) : vehicles),
    [vehicles, inStockOnly],
  );
  const unitsInStock = vehicles.reduce((sum, v) => sum + v.quantity, 0);

  /** Run an API call; on an expired session, log out instead of showing an error. */
  async function attempt(action, successMessage) {
    try {
      const result = await action();
      if (successMessage) setToast({ kind: 'success', message: successMessage });
      return result;
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) logout();
      throw err;
    }
  }

  async function handlePurchase(vehicle) {
    setBusyId(vehicle.id);
    try {
      replace(await attempt(() => vehiclesApi.purchase(vehicle.id), `Purchased ${vehicle.make} ${vehicle.model}`));
    } catch (err) {
      setToast({ kind: 'error', message: err.message });
      reload(); // stock may have changed under us; show the real numbers
    } finally {
      setBusyId(null);
    }
  }

  async function handleCreate(payload) {
    await attempt(() => vehiclesApi.create(payload), `Added ${payload.make} ${payload.model}`);
    closeDialog();
    reload();
  }

  async function handleEdit(payload) {
    replace(await attempt(() => vehiclesApi.update(dialog.vehicle.id, payload), 'Changes saved'));
    closeDialog();
  }

  async function handleRestock(quantity) {
    const { vehicle } = dialog;
    replace(await attempt(() => vehiclesApi.restock(vehicle.id, quantity), `Restocked ${vehicle.make} ${vehicle.model} (+${quantity})`));
    closeDialog();
  }

  async function handleDelete() {
    const { vehicle } = dialog;
    try {
      await attempt(() => vehiclesApi.remove(vehicle.id), `Deleted ${vehicle.make} ${vehicle.model}`);
      remove(vehicle.id);
    } catch (err) {
      setToast({ kind: 'error', message: err.message });
    }
    closeDialog();
  }

  const filtering = hasActiveFilters(filters) || inStockOnly;

  return (
    <div className="min-h-dvh">
      <AppHeader />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="type-badge text-4xl sm:text-5xl">On the lot</h1>
            <p className="mt-2 text-mute" aria-live="polite">
              {loading
                ? 'Loading inventory…'
                : `${visible.length} ${visible.length === 1 ? 'model' : 'models'} shown, ${unitsInStock} ${unitsInStock === 1 ? 'unit' : 'units'} in stock`}
            </p>
          </div>
          {isAdmin && (
            <button type="button" className="btn-paint" onClick={() => setDialog({ type: 'create' })}>
              Add vehicle
            </button>
          )}
        </div>

        <FilterBar filters={filters} onChange={setFilters} inStockOnly={inStockOnly} onInStockOnlyChange={setInStockOnly} />

        {error && (
          <div role="alert" className="mt-6 rounded-md border border-sold/40 bg-paper p-4 text-sold">
            <p className="font-semibold">Couldn’t load vehicles: {error}</p>
            <button type="button" className="mt-2 text-sm font-semibold underline" onClick={reload}>
              Try again
            </button>
          </div>
        )}

        {!loading && !error && visible.length === 0 && (
          <div className="mt-10 rounded-md border-2 border-dashed border-concrete-deep p-10 text-center">
            {filtering ? (
              <>
                <p className="type-badge text-2xl">No vehicles match these filters</p>
                <p className="mt-2 text-mute">Widen the price range or clear the filters to see the whole lot.</p>
              </>
            ) : (
              <>
                <p className="type-badge text-2xl">The lot is empty</p>
                <p className="mt-2 text-mute">
                  {isAdmin ? 'Add your first vehicle to start selling.' : 'No vehicles yet. Check back after the next delivery.'}
                </p>
                {isAdmin && (
                  <button type="button" className="btn-paint mt-5" onClick={() => setDialog({ type: 'create' })}>
                    Add vehicle
                  </button>
                )}
              </>
            )}
          </div>
        )}

        <ul className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {visible.map((vehicle, index) => (
            <li
              key={vehicle.id}
              className="motion-safe:animate-[sticker-in_320ms_ease-out_both]"
              style={{ animationDelay: `${Math.min(index, 12) * 35}ms` }}
            >
              <VehicleCard
                vehicle={vehicle}
                isAdmin={isAdmin}
                busy={busyId === vehicle.id}
                onPurchase={handlePurchase}
                onEdit={(v) => setDialog({ type: 'edit', vehicle: v })}
                onRestock={(v) => setDialog({ type: 'restock', vehicle: v })}
                onDelete={(v) => setDialog({ type: 'delete', vehicle: v })}
              />
            </li>
          ))}
        </ul>
      </main>

      {dialog?.type === 'create' && (
        <Modal title="Add a vehicle" onClose={closeDialog}>
          <VehicleForm onSubmit={handleCreate} onCancel={closeDialog} />
        </Modal>
      )}
      {dialog?.type === 'edit' && (
        <Modal title={`Edit ${dialog.vehicle.make} ${dialog.vehicle.model}`} onClose={closeDialog}>
          <VehicleForm initial={dialog.vehicle} onSubmit={handleEdit} onCancel={closeDialog} />
        </Modal>
      )}
      {dialog?.type === 'restock' && (
        <Modal title="Restock" size="sm" onClose={closeDialog}>
          <RestockForm vehicle={dialog.vehicle} onSubmit={handleRestock} onCancel={closeDialog} />
        </Modal>
      )}
      {dialog?.type === 'delete' && (
        <Modal title="Delete this vehicle?" size="sm" onClose={closeDialog}>
          <p className="text-[15px] text-mute">
            {dialog.vehicle.make} {dialog.vehicle.model} will be removed from the inventory, including its{' '}
            {dialog.vehicle.quantity} units in stock. This can’t be undone.
          </p>
          <div className="mt-5 flex justify-end gap-2">
            <button type="button" className="btn-ghost" onClick={closeDialog}>
              Keep it
            </button>
            <button type="button" className="btn-danger" onClick={handleDelete}>
              Delete vehicle
            </button>
          </div>
        </Modal>
      )}

      <Toast toast={toast} onDismiss={dismissToast} />
    </div>
  );
}
