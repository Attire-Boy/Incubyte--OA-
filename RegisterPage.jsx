import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import AuthLayout from './AuthLayout';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      await register(form);
      navigate('/', { replace: true });
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  }

  const set = (key) => (event) => setForm((prev) => ({ ...prev, [key]: event.target.value }));

  return (
    <AuthLayout
      title="Create an account"
      intro="Browse the lot and buy vehicles. Admins can also manage stock."
      footer={
        <>
          Already registered?{' '}
          <Link to="/login" className="font-semibold text-steel underline-offset-4 hover:underline">
            Log in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="register-name" className="field-label">
            Full name
          </label>
          <input id="register-name" autoComplete="name" required className="field" value={form.name} onChange={set('name')} />
        </div>
        <div>
          <label htmlFor="register-email" className="field-label">
            Email
          </label>
          <input id="register-email" type="email" autoComplete="email" required className="field" value={form.email} onChange={set('email')} />
        </div>
        <div>
          <label htmlFor="register-password" className="field-label">
            Password
          </label>
          <input
            id="register-password"
            type="password"
            autoComplete="new-password"
            required
            minLength={8}
            aria-describedby="register-password-hint"
            className="field"
            value={form.password}
            onChange={set('password')}
          />
          <p id="register-password-hint" className="mt-1 text-sm text-mute">
            At least 8 characters.
          </p>
        </div>
        {error && (
          <p role="alert" className="rounded-md bg-sold/10 px-3 py-2 text-sm text-sold">
            {error}
          </p>
        )}
        <button type="submit" className="btn-primary w-full" disabled={submitting}>
          {submitting ? 'Creating account…' : 'Create account'}
        </button>
      </form>
    </AuthLayout>
  );
}
