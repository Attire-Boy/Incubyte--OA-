import { useEffect } from 'react';

/** Single status message pinned to the bottom of the screen. */
export default function Toast({ toast, onDismiss }) {
  useEffect(() => {
    if (!toast) return undefined;
    const timer = setTimeout(onDismiss, 4000);
    return () => clearTimeout(timer);
  }, [toast, onDismiss]);

  if (!toast) return null;
  const tone = toast.kind === 'error' ? 'border-sold' : 'border-paint';

  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-4 z-50 flex justify-center px-4">
      <div
        role={toast.kind === 'error' ? 'alert' : 'status'}
        className={`pointer-events-auto flex max-w-md items-center gap-3 rounded-md border-l-[6px] ${tone} bg-asphalt px-4 py-3 text-[15px] text-paper shadow-lg`}
      >
        <span>{toast.message}</span>
        <button type="button" onClick={onDismiss} className="ml-2 text-sm font-semibold text-paint">
          Dismiss
        </button>
      </div>
    </div>
  );
}
