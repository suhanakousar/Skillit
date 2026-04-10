import { useMemo } from 'react';

interface Props {
  activityByDate?: Record<string, number>;
  current: number;
  max: number;
}

export default function StreakCalendar({ activityByDate = {}, current, max }: Props) {
  const days = useMemo(() => {
    const today = new Date();
    const out: { date: string; count: number }[] = [];
    for (let i = 364; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      out.push({ date: key, count: activityByDate[key] ?? 0 });
    }
    return out;
  }, [activityByDate]);

  const intensity = (count: number) => {
    if (count === 0) return 'bg-ink-700';
    if (count === 1) return 'bg-brand-700/60';
    if (count <= 3) return 'bg-brand-500/70';
    if (count <= 6) return 'bg-brand-500';
    return 'bg-brand-200';
  };

  return (
    <div className="rounded-xl border border-white/5 bg-ink-800 p-5">
      <div className="mb-4 flex items-baseline justify-between">
        <div>
          <h3 className="text-sm font-medium text-white">Activity</h3>
          <p className="text-xs text-white/50">Last 365 days</p>
        </div>
        <div className="flex gap-4 text-xs text-white/60">
          <span>
            Current: <strong className="text-orange-300">{current}🔥</strong>
          </span>
          <span>
            Longest: <strong className="text-brand-200">{max}</strong>
          </span>
        </div>
      </div>
      <div className="grid grid-flow-col grid-rows-7 gap-[3px] overflow-x-auto scrollbar-thin">
        {days.map((d) => (
          <div
            key={d.date}
            title={`${d.date}: ${d.count} activities`}
            className={`h-3 w-3 rounded-sm ${intensity(d.count)}`}
          />
        ))}
      </div>
    </div>
  );
}
