import { AnimatePresence, motion } from 'framer-motion';
import { useToastStore, type ToastKind } from '../store/toast';

const STYLES: Record<ToastKind, string> = {
  success: 'border-emerald-500/50 bg-emerald-500/10 text-emerald-100',
  error: 'border-red-500/50 bg-red-500/10 text-red-100',
  info: 'border-brand-500/50 bg-brand-500/10 text-brand-100',
};

const ICONS: Record<ToastKind, string> = {
  success: '✓',
  error: '✗',
  info: '•',
};

export default function Toaster() {
  const toasts = useToastStore((s) => s.toasts);
  const dismiss = useToastStore((s) => s.dismiss);

  return (
    <div className="pointer-events-none fixed top-4 right-4 z-[100] flex w-80 flex-col gap-2">
      <AnimatePresence>
        {toasts.map((t) => (
          <motion.div
            key={t.id}
            layout
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 40 }}
            transition={{ duration: 0.2 }}
            className={`pointer-events-auto rounded-xl border bg-ink-800 p-3 shadow-lg backdrop-blur ${STYLES[t.kind]}`}
          >
            <div className="flex items-start gap-2">
              <span className="mt-0.5 font-mono text-sm">{ICONS[t.kind]}</span>
              <div className="flex-1 text-sm">
                <div className="font-medium">{t.title}</div>
                {t.description && <div className="mt-0.5 text-xs opacity-80">{t.description}</div>}
              </div>
              <button
                onClick={() => dismiss(t.id)}
                className="text-xs opacity-50 hover:opacity-100"
              >
                ✕
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
