import { useEffect, useId } from 'react';

/** Accessible dialog: closes on Escape or backdrop click, locks page scroll. */
export default function Modal({ title, onClose, children, size = 'md' }) {
  const titleId = useId();

  useEffect(() => {
    const onKey = (event) => event.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = previousOverflow;
    };
  }, [onClose]);

  const width = size === 'sm' ? 'max-w-sm' : 'max-w-2xl';

  return (
    <div
      className="fixed inset-0 z-40 flex items-end justify-center bg-asphalt/60 p-0 sm:items-center sm:p-4"
      onMouseDown={(event) => event.target === event.currentTarget && onClose()}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        className={`max-h-[92dvh] w-full ${width} overflow-y-auto rounded-t-lg bg-paper p-5 shadow-xl sm:rounded-lg sm:p-6`}
      >
        <div className="mb-5 flex items-start justify-between gap-4">
          <h2 id={titleId} className="type-badge text-xl">
            {title}
          </h2>
          <button type="button" onClick={onClose} className="-m-1 rounded p-1 text-mute hover:text-asphalt" aria-label="Close">
            <svg viewBox="0 0 20 20" className="size-5" aria-hidden="true">
              <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
