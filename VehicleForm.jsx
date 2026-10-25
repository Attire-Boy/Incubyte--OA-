import { useState } from 'react';
import { CATEGORIES } from '../utils/format';

const BLANK = { make: '', model: '', category: '', price: '', quantity: '', year: '', color: '', image_url: '', description: '' };

function toFormState(initial) {
  if (!initial) return BLANK;
  return Object.fromEntries(Object.keys(BLANK).map((key) => [key, initial[key] ?? '']));
}

function validate(values) {
  const errors = {};
  if (!values.make.trim()) errors.make = 'Make is required';
  if (!values.model.trim()) errors.model = 'Model is required';
  if (!values.category) errors.category = 'Choose a category';
  if (values.price === '' || Number(values.price) <= 0) errors.price = 'Price must be greater than 0';
  if (values.quantity === '' || !Number.isInteger(Number(values.quantity)) || Number(values.quantity) < 0) {
    errors.quantity = 'Quantity must be a whole number, 0 or more';
  }
  if (values.year !== '' && (Number(values.year) < 1886 || Number(values.year) > 2100)) {
    errors.year = 'Enter a year between 1886 and 2100';
  }
  return errors;
}

/** Convert form strings into the API's types; empty optional fields become null. */
function toPayload(values) {
  const optional = (value) => (String(value).trim() === '' ? null : String(value).trim());
  return {
    make: values.make.trim(),
    model: values.model.trim(),
    category: values.category,
    price: Number(values.price),
    quantity: Number(values.quantity),
    year: values.year === '' ? null : Number(values.year),
    color: optional(values.color),
    image_url: optional(values.image_url),
    description: optional(values.description),
  };
}

function Field({ id, label, error, children, className = '' }) {
  return (
    <div className={className}>
      <label htmlFor={id} className="field-label">
        {label}
      </label>
      {children}
      {error && (
        <p id={`${id}-error`} className="mt-1 text-sm text-sold">
          {error}
        </p>
      )}
    </div>
  );
}

export default function VehicleForm({ initial, onSubmit, onCancel }) {
  const [values, setValues] = useState(() => toFormState(initial));
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [saving, setSaving] = useState(false);
  const isEdit = Boolean(initial);
  const categories = values.category && !CATEGORIES.includes(values.category)
    ? [values.category, ...CATEGORIES]
    : CATEGORIES;

  const update = (key) => (event) => setValues((prev) => ({ ...prev, [key]: event.target.value }));
  const inputProps = (key) => ({
    id: `vehicle-${key}`,
    value: values[key],
    onChange: update(key),
    'aria-invalid': Boolean(errors[key]),
    'aria-describedby': errors[key] ? `vehicle-${key}-error` : undefined,
    className: 'field',
  });

  async function handleSubmit(event) {
    event.preventDefault();
    const found = validate(values);
    setErrors(found);
    if (Object.keys(found).length) return;
    setSaving(true);
    setServerError('');
    try {
      await onSubmit(toPayload(values));
    } catch (error) {
      setServerError(error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="grid gap-4 sm:grid-cols-2">
      <Field id="vehicle-make" label="Make" error={errors.make}>
        <input {...inputProps('make')} autoFocus placeholder="Toyota" />
      </Field>
      <Field id="vehicle-model" label="Model" error={errors.model}>
        <input {...inputProps('model')} placeholder="Corolla" />
      </Field>
      <Field id="vehicle-category" label="Category" error={errors.category}>
        <select {...inputProps('category')}>
          <option value="">Choose a category</option>
          {categories.map((category) => (
            <option key={category}>{category}</option>
          ))}
        </select>
      </Field>
      <Field id="vehicle-year" label="Year (optional)" error={errors.year}>
        <input {...inputProps('year')} type="number" inputMode="numeric" placeholder="2025" />
      </Field>
      <Field id="vehicle-price" label="Price (USD)" error={errors.price}>
        <input {...inputProps('price')} type="number" inputMode="decimal" min="1" step="1" placeholder="21500" />
      </Field>
      <Field id="vehicle-quantity" label="Quantity in stock" error={errors.quantity}>
        <input {...inputProps('quantity')} type="number" inputMode="numeric" min="0" step="1" placeholder="5" />
      </Field>
      <Field id="vehicle-color" label="Color (optional)">
        <input {...inputProps('color')} placeholder="Midnight blue" />
      </Field>
      <Field id="vehicle-image_url" label="Photo URL (optional)">
        <input {...inputProps('image_url')} type="url" placeholder="https://…" />
      </Field>
      <Field id="vehicle-description" label="Notes (optional)" className="sm:col-span-2">
        <textarea {...inputProps('description')} rows={2} placeholder="One owner, full service history" />
      </Field>

      {serverError && (
        <p role="alert" className="rounded-md bg-sold/10 px-3 py-2 text-sm text-sold sm:col-span-2">
          {serverError}
        </p>
      )}

      <div className="flex justify-end gap-2 sm:col-span-2">
        <button type="button" className="btn-ghost" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn-primary" disabled={saving}>
          {saving ? 'Saving…' : isEdit ? 'Save changes' : 'Add vehicle'}
        </button>
      </div>
    </form>
  );
}
