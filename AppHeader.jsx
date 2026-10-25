import { useAuth } from '../context/AuthContext';

export function Wordmark({ light = false }) {
  return (
    <span className={`type-badge text-2xl ${light ? 'text-paper' : 'text-asphalt'}`}>
      Lot<span className="text-paint-deep">line</span>
    </span>
  );
}

export default function AppHeader() {
  const { user, isAdmin, logout } = useAuth();

  return (
    <header className="bg-paper">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Wordmark />
        <div className="flex items-center gap-3 text-sm">
          <div className="hidden text-right sm:block">
            <p className="font-semibold">{user?.name}</p>
            <p className="text-mute">{isAdmin ? 'Admin' : 'Buyer'}</p>
          </div>
          <button type="button" className="btn-ghost px-3 py-2 text-sm" onClick={logout}>
            Log out
          </button>
        </div>
      </div>
      <div className="lane-line bg-asphalt" aria-hidden="true" />
    </header>
  );
}
