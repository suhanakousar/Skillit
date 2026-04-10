import { useSearchParams } from 'react-router-dom';
import { useMemo } from 'react';

interface Props {
  totalByDifficulty?: Record<number, number>;
  totalByTag?: Record<string, number>;
  availableTags?: string[];
}

const DIFFICULTY_LABELS: Record<number, string> = {
  1: '★',
  2: '★★',
  3: '★★★',
  4: '★★★★',
  5: '★★★★★',
};

const STATUSES = ['all', 'solved', 'attempted', 'unsolved'] as const;

export default function ProblemFilters({
  totalByDifficulty = {},
  totalByTag = {},
  availableTags = [],
}: Props) {
  const [params, setParams] = useSearchParams();

  const selectedDifficulty = params.get('difficulty');
  const selectedTags = useMemo(() => (params.get('tags') || '').split(',').filter(Boolean), [params]);
  const selectedStatus = params.get('status') || 'all';

  const toggleDifficulty = (d: number) => {
    const next = new URLSearchParams(params);
    if (selectedDifficulty === String(d)) next.delete('difficulty');
    else next.set('difficulty', String(d));
    setParams(next);
  };

  const toggleTag = (tag: string) => {
    const next = new URLSearchParams(params);
    const now = selectedTags.includes(tag)
      ? selectedTags.filter((t) => t !== tag)
      : [...selectedTags, tag];
    if (now.length === 0) next.delete('tags');
    else next.set('tags', now.join(','));
    setParams(next);
  };

  const setStatus = (status: string) => {
    const next = new URLSearchParams(params);
    if (status === 'all') next.delete('status');
    else next.set('status', status);
    setParams(next);
  };

  const clearAll = () => setParams(new URLSearchParams());

  const hasAny = selectedDifficulty || selectedTags.length > 0 || selectedStatus !== 'all';

  return (
    <aside className="w-full space-y-5 rounded-2xl border border-white/5 bg-ink-800 p-4 lg:w-60">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-medium uppercase tracking-wider text-white/60">Filters</h3>
        {hasAny && (
          <button
            onClick={clearAll}
            className="text-[10px] text-brand-200 hover:text-brand-100"
          >
            Clear
          </button>
        )}
      </div>

      <div>
        <div className="mb-2 text-[10px] uppercase tracking-wider text-white/40">Status</div>
        <div className="flex flex-wrap gap-1">
          {STATUSES.map((s) => (
            <button
              key={s}
              onClick={() => setStatus(s)}
              className={`rounded-full px-2 py-1 text-[10px] capitalize ${
                selectedStatus === s
                  ? 'bg-brand-600 text-white'
                  : 'bg-ink-700 text-white/60 hover:bg-ink-900'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div>
        <div className="mb-2 text-[10px] uppercase tracking-wider text-white/40">Difficulty</div>
        <div className="space-y-1">
          {[1, 2, 3, 4, 5].map((d) => {
            const selected = selectedDifficulty === String(d);
            const count = totalByDifficulty[d] ?? 0;
            return (
              <button
                key={d}
                onClick={() => toggleDifficulty(d)}
                className={`flex w-full items-center justify-between rounded px-2 py-1.5 text-xs ${
                  selected
                    ? 'bg-brand-600/30 text-white'
                    : 'text-white/60 hover:bg-white/5'
                }`}
              >
                <span className="font-mono text-yellow-300">{DIFFICULTY_LABELS[d]}</span>
                <span className="text-[10px] text-white/40">{count}</span>
              </button>
            );
          })}
        </div>
      </div>

      {availableTags.length > 0 && (
        <div>
          <div className="mb-2 text-[10px] uppercase tracking-wider text-white/40">Tags</div>
          <div className="flex max-h-48 flex-wrap gap-1 overflow-y-auto scrollbar-thin">
            {availableTags.map((tag) => {
              const on = selectedTags.includes(tag);
              return (
                <button
                  key={tag}
                  onClick={() => toggleTag(tag)}
                  className={`rounded-full px-2 py-0.5 text-[10px] ${
                    on
                      ? 'bg-brand-600 text-white'
                      : 'bg-ink-700 text-white/60 hover:bg-ink-900'
                  }`}
                >
                  {tag} <span className="opacity-50">({totalByTag[tag] ?? 0})</span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </aside>
  );
}
