import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import VehicleForm from './VehicleForm';

describe('VehicleForm', () => {
  it('submits typed, numeric values for a new vehicle', async () => {
    const onSubmit = vi.fn().mockResolvedValue();
    render(<VehicleForm onSubmit={onSubmit} onCancel={() => {}} />);

    await userEvent.type(screen.getByLabelText(/^make/i), 'Kia');
    await userEvent.type(screen.getByLabelText(/^model/i), 'Seltos');
    await userEvent.selectOptions(screen.getByLabelText(/category/i), 'SUV');
    await userEvent.type(screen.getByLabelText(/price/i), '19999');
    await userEvent.type(screen.getByLabelText(/quantity/i), '4');
    await userEvent.click(screen.getByRole('button', { name: /add vehicle/i }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ make: 'Kia', model: 'Seltos', category: 'SUV', price: 19999, quantity: 4 }),
    );
  });

  it('blocks submission and explains when required fields are missing', async () => {
    const onSubmit = vi.fn();
    render(<VehicleForm onSubmit={onSubmit} onCancel={() => {}} />);
    await userEvent.click(screen.getByRole('button', { name: /add vehicle/i }));
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByText(/make is required/i)).toBeInTheDocument();
  });

  it('rejects a non-positive price', async () => {
    const onSubmit = vi.fn();
    render(
      <VehicleForm
        initial={{ make: 'A', model: 'B', category: 'Sedan', price: 0, quantity: 1 }}
        onSubmit={onSubmit}
        onCancel={() => {}}
      />,
    );
    await userEvent.click(screen.getByRole('button', { name: /save changes/i }));
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByText(/price must be greater than 0/i)).toBeInTheDocument();
  });

  it('pre-fills values and says "Save changes" when editing', () => {
    render(
      <VehicleForm
        initial={{ make: 'Ford', model: 'F-150', category: 'Truck', price: 38900, quantity: 3 }}
        onSubmit={() => {}}
        onCancel={() => {}}
      />,
    );
    expect(screen.getByLabelText(/^make/i)).toHaveValue('Ford');
    expect(screen.getByRole('button', { name: /save changes/i })).toBeInTheDocument();
  });
});
