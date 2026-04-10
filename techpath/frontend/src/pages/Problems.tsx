import { useEffect, useMemo, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { problemsApi } from '../api/endpoints';
import type { ProblemSummary } from '../types';
import ProblemFilters from '../components/ProblemFilters';

const DIFFICULTY_LABELS: Record<number, { label: string; className: string; dot: string }> = {
  1: { label: 'Easy', className: 'text-emerald-300 bg-emerald-500/10 ring-1 ring-emerald-500/20', dot: 'bg-emerald-400' },
  2: { label: 'Easy+', className: 'text-emerald-200 bg-emerald-500/10 ring-1 ring-emerald-500/20', dot: 'bg-emerald-300' },
  3: { label: 'Medium', className: 'text-yellow-300 bg-yellow-500/10 ring-1 ring-yellow-500/20', dot: 'bg-yellow-400' },
  4: { label: 'Hard-', className: 'text-orange-300 bg-orange-500/10 ring-1 ring-orange-500/20', dot: 'bg-orange-400' },
  5: { label: 'Hard', className: 'text-red-300 bg-red-500/10 ring-1 ring-red-500/20', dot: 'bg-red-400' },
};

export default function Problems() {
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [params, setParams] = useSearchParams();

  const difficulty = params.get('difficulty') ? Number(params.get('difficulty')) : undefined;
  const tagsParam = params.get('tags');
  const firstTag = tagsParam?.split(',')[0];
  const q = params.get('q') ?? '';

  useEffect(() => {
    setLoading(true);
    problemsApi
      .list({ difficulty, tag: firstTag, limit: 500 })
      .then((res) => {
        setProblems(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [difficulty, firstTag]);

  const filtered = useMemo(() => {
    let out = problems;
    if (tagsParam) {
      const tags = tagsParam.split(',').filter(Boolean);
      if (tags.length > 1) out = out.filter((p) => tags.every((t) => p.tags.includes(t)));
    }
    if (q.trim()) {
      const needle = q.trim().toLowerCase();
      out = out.filter(
        (p) =>
          p.title.toLowerCase().includes(needle) ||
          p.tags.some((t) => t.toLowerCase().includes(needle)),
      );
    }
    return out;
  }, [problems, tagsParam, q]);

  const totals = useMemo(() => {
    const byDifficulty: Record<number, number> = {};
    const byTag: Record<string, number> = {};
    const tagSet = new Set<string>();
    for (const p of problems) {
      byDifficulty[p.difficulty] = (byDifficulty[p.difficulty] ?? 0) + 1;
      for (const t of p.tags) {
        byTag[t] = (byTag[t] ?? 0) + 1;
        tagSet.add(t);
      }
    }
    return { byDifficulty, byTag, tags: [...tagSet].sort() };
  }, [problems]);

  const setQuery = (value: string) => {
    const next = new URLSearchParams(params);
    if (value) next.set('q', value);
    else next.delete('q');
    setParams(next, { replace: true });
  };

  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-6 lg:px-6">
      <header className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Practice Arena</h1>
          <p className="mt-1 text-sm text-white/60">
            Solve problems, earn XP, unlock badges. Fast feedback, real test cases.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <StatPill label="Total" value={problems.length} accent="brand" />
          <StatPill label="Easy" value={(totals.byDifficulty[1] ?? 0) + (totals.byDifficulty[2] ?? 0)} accent="emerald" />
          <StatPill label="Medium" value={totals.byDifficulty[3] ?? 0} accent="yellow" />
          <StatPill label="Hard" value={(totals.byDifficulty[4] ?? 0) + (totals.byDifficulty[5] ?? 0)} accent="red" />
        </div>
      </header>

      <div className="flex flex-col gap-6 lg:flex-row">
        <div className="lg:w-64 lg:flex-shrink-0">
          <ProblemFilters
            totalByDifficulty={totals.byDifficulty}
            totalByTag={totals.byTag}
            availableTags={totals.tags}
          />
        </div>

        <div className="flex-1 space-y-4">
          {/* Search bar */}
          <div className="relative">
            <input
              type="text"
              value={q}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by title or tag…"
              className="w-full rounded-xl border border-white/10 bg-ink-800 py-3 pl-10 pr-4 text-sm text-white placeholder-white/40 outline-none transition focus:border-brand-500 focus:bg-ink-800/80"
            />
            <svg
              className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-white/40"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-4.3-4.3M10.5 18a7.5 7.5 0 1 1 0-15 7.5 7.5 0 0 1 0 15Z" />
            </svg>
            {q && (
              <button
                onClick={() => setQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 rounded-full p-1 text-white/40 hover:bg-white/10 hover:text-white/80"
                aria-label="Clear search"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>

          {/* Result count */}
          <div className="flex items-center justify-between text-xs text-white/50">
            <span>
              Showing <span className="font-medium text-white/80">{filtered.length}</span>
              {filtered.length !== problems.length && (
                <> of <span className="text-white/60">{problems.length}</span></>
              )}{' '}
              problems
            </span>
          </div>

          {/* Table */}
          <div className="overflow-hidden rounded-2xl border border-white/5 bg-ink-800 shadow-xl shadow-black/20">
            <table className="w-full text-sm">
              <thead className="border-b border-white/5 bg-ink-900/50 text-[11px] uppercase tracking-wider text-white/40">
                <tr>
                  <th className="w-12 px-4 py-3 text-left font-medium">#</th>
                  <th className="px-4 py-3 text-left font-medium">Title</th>
                  <th className="px-4 py-3 text-left font-medium">Difficulty</th>
                  <th className="px-4 py-3 text-left font-medium">Tags</th>
                  <th className="px-4 py-3 text-right font-medium">Reward</th>
                </tr>
              </thead>
              <tbody>
                {loading && (
                  <>
                    {Array.from({ length: 8 }).map((_, i) => (
                      <tr key={i} className="border-t border-white/5">
                        <td className="px-4 py-4"><div className="h-3 w-6 animate-pulse rounded bg-white/10" /></td>
                        <td className="px-4 py-4"><div className="h-3 w-40 animate-pulse rounded bg-white/10" /></td>
                        <td className="px-4 py-4"><div className="h-5 w-16 animate-pulse rounded-full bg-white/10" /></td>
                        <td className="px-4 py-4"><div className="h-3 w-24 animate-pulse rounded bg-white/10" /></td>
                        <td className="px-4 py-4 text-right"><div className="ml-auto h-3 w-10 animate-pulse rounded bg-white/10" /></td>
                      </tr>
                    ))}
                  </>
                )}

                {!loading && filtered.map((p, idx) => {
                  const diff = DIFFICULTY_LABELS[p.difficulty];
                  return (
                    <tr
                      key={p.id}
                      className="group border-t border-white/5 transition hover:bg-gradient-to-r hover:from-brand-600/5 hover:to-transparent"
                    >
                      <td className="px-4 py-4 text-[11px] text-white/40">{idx + 1}</td>
                      <td className="px-4 py-4">
                        <Link
                          to={`/problems/${p.id}`}
                          className="font-medium text-white transition group-hover:text-brand-200"
                        >
                          {p.title}
                        </Link>
                      </td>
                      <td className="px-4 py-4">
                        <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[10px] font-medium ${diff.className}`}>
                          <span className={`h-1.5 w-1.5 rounded-full ${diff.dot}`} />
                          {diff.label}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex flex-wrap gap-1">
                          {p.tags.slice(0, 3).map((t) => (
                            <span
                              key={t}
                              className="rounded-md bg-brand-600/10 px-2 py-0.5 text-[10px] font-medium text-brand-200 ring-1 ring-inset ring-brand-500/20"
                            >
                              {t}
                            </span>
                          ))}
                          {p.tags.length > 3 && (
                            <span className="rounded-md bg-white/5 px-2 py-0.5 text-[10px] text-white/40">
                              +{p.tags.length - 3}
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-brand-200">
                          <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 0 0 .95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 0 0-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.539 1.118l-2.8-2.034a1 1 0 0 0-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 0 0-.363-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 0 0 .951-.69l1.07-3.292Z" />
                          </svg>
                          {p.xp_reward}
                        </span>
                      </td>
                    </tr>
                  );
                })}

                {!loading && filtered.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-4 py-16">
                      <div className="flex flex-col items-center gap-2 text-center">
                        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
                          <svg className="h-6 w-6 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-4.3-4.3M10.5 18a7.5 7.5 0 1 1 0-15 7.5 7.5 0 0 1 0 15Z" />
                          </svg>
                        </div>
                        <p className="text-sm text-white/60">No problems match these filters</p>
                        <p className="text-xs text-white/40">Try clearing the search or removing a tag filter.</p>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatPill({ label, value, accent }: { label: string; value: number; accent: 'brand' | 'emerald' | 'yellow' | 'red' }) {
  const colors: Record<string, string> = {
    brand: 'bg-brand-600/10 text-brand-200 ring-brand-500/20',
    emerald: 'bg-emerald-500/10 text-emerald-300 ring-emerald-500/20',
    yellow: 'bg-yellow-500/10 text-yellow-300 ring-yellow-500/20',
    red: 'bg-red-500/10 text-red-300 ring-red-500/20',
  };
  return (
    <div className={`flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-medium ring-1 ring-inset ${colors[accent]}`}>
      <span className="opacity-70">{label}</span>
      <span className="font-bold">{value}</span>
    </div>
  );
}
