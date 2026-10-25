import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import LoginPage from './LoginPage';

function renderLogin() {
  render(
    <MemoryRouter initialEntries={['/login']}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<p>Dashboard home</p>} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  );
}

function respond(status, body) {
  global.fetch = vi.fn().mockResolvedValue({
    ok: status < 300,
    status,
    json: () => Promise.resolve(body),
  });
}

describe('LoginPage', () => {
  beforeEach(() => localStorage.clear());

  it('logs in, stores the token and goes to the dashboard', async () => {
    respond(200, {
      access_token: 'tok',
      token_type: 'bearer',
      user: { id: 1, name: 'Jane', email: 'jane@example.com', is_admin: false },
    });
    renderLogin();
    await userEvent.type(screen.getByLabelText(/email/i), 'jane@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'Str0ngPass!');
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    expect(await screen.findByText('Dashboard home')).toBeInTheDocument();
    expect(localStorage.getItem('lotline.token')).toBe('tok');
  });

  it('shows the server error when credentials are wrong', async () => {
    respond(401, { detail: 'Invalid email or password' });
    renderLogin();
    await userEvent.type(screen.getByLabelText(/email/i), 'jane@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'nope-nope');
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password');
  });
});
