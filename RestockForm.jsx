import { useState } from 'react';

export default function RestockForm({ vehicle, onSubmit, onCancel }) {
  const [quantity, setQuantity] = useState('1');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    const amount = Number(quantity);
    if (!Number.isInteger(amount) || amount < 1) {
      setError('Enter a whole number of 1 or more');
      return;
    }
    setSaving(true);
    try {
      await onSubmit(amount);
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <p className="mb-4 text-[15px] text-mute">
        {vehicle.make} {vehicle.model} currently has {vehicle.quantity} on the lot.
      </p>
      <label htmlFor="restock-quantity" className="field-label">
        Units arriving
      </label>
      <input
        id="restock-quantity"
        type="number"
        min="1"
        step="1"
        inputMode="numeric"
        autoFocus
        className="field"
        value={quantity}
        onChange={(event) => setQuantity(event.target.value)}
      />
      {error && (
        <p role="alert" className="mt-1 text-sm text-sold">
          {error}
        </p>
      )}
      <div className="mt-5 flex justify-end gap-2">
        <button type="button" className="btn-ghost" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn-primary" disabled={saving}>
          {saving ? 'Restocking…' : 'Restock'}
        </button>
      </div>
    </form>
  );
}
