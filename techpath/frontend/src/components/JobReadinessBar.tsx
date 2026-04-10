import type { ReadinessArea } from '../types';

interface Props {
  overall: number;
  breakdown: ReadinessArea[];
}

export default function JobReadinessBar({ overall, breakdown }: Props) {
  const color = overall >= 80 ? '#639922' : overall >= 50 ? '#BA7517' : '#D85A30';
  return (
    <div className="rounded-2xl border border-white/5 bg-ink-800 p-6">
      <div className="mb-4 flex items-baseline gap-3">
        <div className="text-5xl font-bold text-white">{overall}</div>
        <div className="text-sm text-white/60">% job ready</div>
      </div>
      <div className="mb-5 h-2 overflow-hidden rounded-full bg-ink-700">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${overall}%`, background: color }}
        />
      </div>
      <div className="space-y-3">
        {breakdown.map((b) => (
          <div key={b.area}>
            <div className="mb-1 flex items-center justify-between text-xs">
              <span className="font-medium text-white/80 capitalize">{b.area}</span>
              <span className="text-white/50">
                {b.current}% / {b.required}%
              </span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-ink-700">
              <div
                className="h-full rounded-full"
                style={{
                  width: `${Math.min(100, b.current)}%`,
                  background: b.current >= b.required ? '#639922' : '#534AB7',
                }}
              />
            </div>
            {b.gap > 0 && <div className="mt-1 text-[11px] text-white/50">{b.action}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
