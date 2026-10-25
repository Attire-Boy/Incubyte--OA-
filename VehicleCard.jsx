import { formatPrice, stockLabel } from '../utils/format';

/**
 * A vehicle rendered as a dealership window sticker: who made it, what it
 * costs, how many are on the lot, and the one action a buyer can take.
 */
export default function VehicleCard({ vehicle, isAdmin, busy = false, onPurchase, onEdit, onDelete, onRestock }) {
  const { make, model, category, price, quantity, year, color, image_url: imageUrl, description } = vehicle;
  const soldOut = quantity <= 0;

  let purchaseLabel = 'Purchase';
  if (soldOut) purchaseLabel = 'Sold out';
  if (busy) purchaseLabel = 'Purchasing…';

  return (
    <article
      className="flex flex-col overflow-hidden rounded-sm border-2 border-asphalt bg-paper shadow-[4px_4px_0_var(--color-asphalt)]"
      aria-label={`${make} ${model}`}
    >
      <header className="flex items-center justify-between bg-asphalt px-4 py-2 text-sm text-paper">
        <span className="font-semibold">{category}</span>
        {year && <span className="tabular-nums text-paper/75">{year}</span>}
      </header>

      {imageUrl && (
        <img src={imageUrl} alt="" className="aspect-[16/9] w-full border-b-2 border-asphalt object-cover" loading="lazy" />
      )}

      <div className="flex flex-1 flex-col gap-4 p-4">
        <div>
          <p className="text-[15px] font-medium text-mute">{make}</p>
          <h3 className="type-badge mt-0.5 text-[1.7rem] break-words">{model}</h3>
          {(color || description) && (
            <p className="mt-2 line-clamp-2 text-sm text-mute">
              {[color, description].filter(Boolean).join('. ')}
            </p>
          )}
        </div>

        <div className="mt-auto flex flex-wrap items-end justify-between gap-x-3 gap-y-2 border-t border-dashed border-concrete-deep pt-3">
          <div>
            <p className="text-xs text-mute">Price</p>
            <p className="type-badge bg-paint px-1.5 py-1 text-2xl tabular-nums">{formatPrice(price)}</p>
          </div>
          <p
            className={`flex items-center gap-1.5 whitespace-nowrap text-sm font-semibold ${soldOut ? 'text-sold' : 'text-stock'}`}
          >
            <span aria-hidden="true" className={`size-2 rounded-full ${soldOut ? 'bg-sold' : 'bg-stock'}`} />
            {stockLabel(quantity)}
          </p>
        </div>

        <button
          type="button"
          className="btn-primary w-full"
          disabled={soldOut || busy}
          onClick={() => onPurchase(vehicle)}
        >
          {purchaseLabel}
        </button>

        {isAdmin && (
          <div className="-mx-1 flex flex-wrap gap-1 border-t border-concrete-deep pt-3 text-sm">
            <button type="button" className="rounded px-2 py-1 font-semibold text-steel hover:bg-concrete" onClick={() => onEdit(vehicle)}>
              Edit
            </button>
            <button type="button" className="rounded px-2 py-1 font-semibold text-steel hover:bg-concrete" onClick={() => onRestock(vehicle)}>
              Restock
            </button>
            <button
              type="button"
              className="ml-auto rounded px-2 py-1 font-semibold text-sold hover:bg-sold/10"
              onClick={() => onDelete(vehicle)}
            >
              Delete
            </button>
          </div>
        )}
      </div>
    </article>
  );
}
