import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { aiApi } from '../api/endpoints';

interface Props {
  problemId: string;
  userCode: string;
}

interface Message {
  role: 'user' | 'assistant';
  level?: number;
  text: string;
}

export default function HintChat({ problemId, userCode }: Props) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const requestHint = async (level: number) => {
    if (level === 3) {
      const ok = confirm(
        'Level 3 is a big spoiler — it reveals the key insight and pseudocode. Try a bit more first?',
      );
      if (!ok) return;
    }

    setLoading(true);
    setMessages((m) => [...m, { role: 'user', text: `Give me a level ${level} hint` }]);
    try {
      const r = await aiApi.hint(problemId, level, userCode);
      setMessages((m) => [...m, { role: 'assistant', level, text: r.text }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: 'assistant', level, text: 'Hint service unavailable right now.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="mb-3 flex w-80 flex-col overflow-hidden rounded-2xl border border-white/10 bg-ink-800 shadow-2xl"
          >
            <header className="flex items-center justify-between border-b border-white/10 bg-ink-700 px-4 py-2">
              <div>
                <div className="text-sm font-medium text-white">AI hint coach</div>
                <div className="text-[10px] text-white/50">Never gives the full answer</div>
              </div>
              <button
                onClick={() => setOpen(false)}
                className="text-white/50 hover:text-white"
              >
                ✕
              </button>
            </header>

            <div className="max-h-80 flex-1 space-y-3 overflow-y-auto p-4 scrollbar-thin">
              {messages.length === 0 && (
                <p className="text-xs text-white/50">
                  Choose a hint level to get a nudge, an approach, or the key insight.
                </p>
              )}
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`rounded-lg p-3 text-xs ${
                    m.role === 'user'
                      ? 'bg-brand-600/20 text-white ml-6'
                      : 'bg-ink-900 text-white/80 mr-6'
                  }`}
                >
                  {m.level && (
                    <div className="mb-1 text-[10px] uppercase tracking-wider text-brand-200">
                      Hint level {m.level}
                    </div>
                  )}
                  {m.text}
                </div>
              ))}
              {loading && (
                <div className="text-[11px] text-white/40">thinking…</div>
              )}
            </div>

            <footer className="grid grid-cols-3 gap-1 border-t border-white/10 bg-ink-700 p-2">
              {[1, 2, 3].map((level) => (
                <button
                  key={level}
                  onClick={() => requestHint(level)}
                  disabled={loading}
                  className="rounded bg-brand-600/20 px-2 py-1.5 text-[10px] font-medium text-brand-200 hover:bg-brand-600/40 disabled:opacity-40"
                >
                  Level {level}
                </button>
              ))}
            </footer>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.button
        onClick={() => setOpen((v) => !v)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="flex h-12 w-12 items-center justify-center rounded-full bg-brand-600 text-xl shadow-lg hover:bg-brand-500"
        title="AI hint coach"
      >
        💡
      </motion.button>
    </div>
  );
}
