import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import type { RoadmapNode } from '../types';

interface Props {
  nodes: RoadmapNode[];
}

const STATE_STYLES: Record<RoadmapNode['state'], string> = {
  completed: 'bg-emerald-500/20 border-emerald-400/50 text-emerald-200',
  active: 'bg-brand-500/20 border-brand-400/60 text-brand-100 shadow-[0_0_24px_rgba(127,119,221,0.35)]',
  unlocked: 'bg-ink-800 border-brand-500/40 text-white hover:bg-brand-600/10',
  locked: 'bg-ink-800 border-white/10 text-white/30',
};

export default function RoadmapTree({ nodes }: Props) {
  const navigate = useNavigate();
  const years = [1, 2, 3, 4];

  return (
    <div className="space-y-6">
      {years.map((year) => {
        const yearNodes = nodes.filter((n) => n.year === year);
        if (yearNodes.length === 0) return null;

        return (
          <div key={year} className="rounded-2xl border border-white/5 bg-ink-800/50 p-5">
            <div className="mb-4 flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-brand-500" />
              <h3 className="text-sm font-medium uppercase tracking-wider text-white/80">
                Year {year}
              </h3>
            </div>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
              {yearNodes.map((n, i) => (
                <motion.button
                  key={n.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.03 }}
                  onClick={() => n.state !== 'locked' && n.track_id && navigate(`/track/${n.track_id}`)}
                  disabled={n.state === 'locked'}
                  className={`rounded-xl border p-3 text-left transition ${STATE_STYLES[n.state]}`}
                >
                  <div className="text-[10px] uppercase tracking-wider opacity-60">
                    {n.domain}
                  </div>
                  <div className="mt-1 text-sm font-medium leading-tight">{n.title}</div>
                  {n.state === 'locked' && (
                    <div className="mt-2 text-[10px] opacity-60">🔒 Prereq locked</div>
                  )}
                  {n.state === 'completed' && (
                    <div className="mt-2 text-[10px]">✓ Done</div>
                  )}
                </motion.button>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
