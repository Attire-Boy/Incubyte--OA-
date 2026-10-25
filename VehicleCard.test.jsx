import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import VehicleCard from './VehicleCard';

const vehicle = {
  id: 7,
  make: 'Toyota',
  model: 'RAV4',
  category: 'SUV',
  price: 29800,
  quantity: 3,
  year: 2025,
  color: 'White',
};

function setup(props = {}) {
  const handlers = {
    onPurchase: vi.fn(),
    onEdit: vi.fn(),
    onDelete: vi.fn(),
    onRestock: vi.fn(),
  };
  render(<VehicleCard vehicle={vehicle} isAdmin={false} {...handlers} {...props} />);
  return handlers;
}

describe('VehicleCard', () => {
  it('shows make, model, price and stock', () => {
    setup();
    expect(screen.getByText('Toyota')).toBeInTheDocument();
    expect(screen.getByText('RAV4')).toBeInTheDocument();
    expect(screen.getByText('$29,800')).toBeInTheDocument();
    expect(screen.getByText('3 on the lot')).toBeInTheDocument();
  });

  it('calls onPurchase with the vehicle when Purchase is clicked', async () => {
    const { onPurchase } = setup();
    await userEvent.click(screen.getByRole('button', { name: /purchase/i }));
    expect(onPurchase).toHaveBeenCalledWith(vehicle);
  });

  it('disables Purchase when quantity is zero', () => {
    setup({ vehicle: { ...vehicle, quantity: 0 } });
    expect(screen.getByRole('button', { name: /sold out/i })).toBeDisabled();
  });

  it('disables Purchase while a purchase is in flight', () => {
    setup({ busy: true });
    expect(screen.getByRole('button', { name: /purchas/i })).toBeDisabled();
  });

  it('hides admin controls for regular users', () => {
    setup();
    expect(screen.queryByRole('button', { name: /edit/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /delete/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /restock/i })).not.toBeInTheDocument();
  });

  it('shows admin controls and wires them up for admins', async () => {
    const { onEdit, onDelete, onRestock } = setup({ isAdmin: true });
    await userEvent.click(screen.getByRole('button', { name: /edit/i }));
    await userEvent.click(screen.getByRole('button', { name: /delete/i }));
    await userEvent.click(screen.getByRole('button', { name: /restock/i }));
    expect(onEdit).toHaveBeenCalledWith(vehicle);
    expect(onDelete).toHaveBeenCalledWith(vehicle);
    expect(onRestock).toHaveBeenCalledWith(vehicle);
  });
});
