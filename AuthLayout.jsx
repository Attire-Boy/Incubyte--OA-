import { Wordmark } from '../components/AppHeader';

/** Split screen: an asphalt lot with painted bays beside the form. */
export default function AuthLayout({ title, intro, children, footer }) {
  return (
    <main className="grid min-h-dvh lg:grid-cols-[1.1fr_1fr]">
      <aside className="relative hidden flex-col bg-asphalt text-paper lg:flex">
        <div className="flex flex-1 flex-col p-10">
          <Wordmark light />
          <div className="mt-auto max-w-md pb-10">
            <p className="type-badge text-5xl leading-[1.02]">Every car on the lot, accounted for.</p>
            <p className="mt-5 max-w-sm text-paper/75">
              Track stock, sell from the floor, and restock when deliveries arrive.
            </p>
          </div>
        </div>
        <div className="parking-bays h-[38%]" aria-hidden="true" />
      </aside>

      <section className="flex flex-col justify-center px-5 py-10 sm:px-10">
        <div className="mx-auto w-full max-w-sm">
          <div className="mb-8 lg:hidden">
            <Wordmark />
          </div>
          <h1 className="type-badge text-3xl">{title}</h1>
          <p className="mt-2 text-mute">{intro}</p>
          <div className="mt-8">{children}</div>
          <p className="mt-6 text-sm text-mute">{footer}</p>
        </div>
      </section>
    </main>
  );
}
