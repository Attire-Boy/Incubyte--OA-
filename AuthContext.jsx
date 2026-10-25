import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { authApi } from '../api/endpoints';
import { tokenStore } from '../api/client';

const USER_KEY = 'lotline.user';
const AuthContext = createContext(null);

function readStoredUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY));
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => (tokenStore.get() ? readStoredUser() : null));

  const startSession = useCallback(({ access_token, user: account }) => {
    tokenStore.set(access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(account));
    setUser(account);
  }, []);

  const logout = useCallback(() => {
    tokenStore.clear();
    localStorage.removeItem(USER_KEY);
    setUser(null);
  }, []);

  const login = useCallback(async (credentials) => startSession(await authApi.login(credentials)), [startSession]);
  const register = useCallback(async (details) => startSession(await authApi.register(details)), [startSession]);

  // Re-validate a remembered session once on load; drop it if the token expired.
  useEffect(() => {
    if (!tokenStore.get()) return;
    authApi.me().then(setUser).catch(logout);
  }, [logout]);

  const value = useMemo(
    () => ({ user, isAdmin: Boolean(user?.is_admin), login, register, logout }),
    [user, login, register, logout],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used inside <AuthProvider>');
  return context;
}
