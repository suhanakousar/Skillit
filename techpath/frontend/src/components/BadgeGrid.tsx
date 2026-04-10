import { motion } from 'framer-motion';
import type { Badge } from '../types';

interface Props {
  earned: Badge[];
  all?: Badge[];
}

export default function BadgeGrid({ earned, all = [] }: Props) {
  const earnedSlugs = new Set(earned.map((b) => b.slug));
  const display = all.length ? all : earned;

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
      {display.map((b) => {
        const isEarned = earnedSlugs.has(b.slug);
        return (
          <motion.div
            key={b.id}
            whileHover={{ scale: 1.03 }}
            className={`group relative rounded-xl border p-4 transition ${
              isEarned
                ? 'border-brand-500/50 bg-brand-600/10'
                : 'border-white/10 bg-ink-800 opacity-50'
            }`}
          >
            <div className="mb-2 text-2xl">{isEarned ? '🏅' : '🔒'}</div>
            <div className="text-sm font-medium text-white">{b.name}</div>
            <div className="mt-1 text-[11px] text-white/50">{b.description}</div>
            {b.xp_bonus > 0 && (
              <div className="mt-2 inline-block rounded-full bg-brand-600/30 px-2 py-0.5 text-[10px] text-brand-100">
                +{b.xp_bonus} XP
              </div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
