import { useEffect, useMemo, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { problemsApi } from '../api/endpoints';
import type { ProblemSummary } from '../types';
import ProblemFilters from '../components/ProblemFilters';

const DIFFICULTY_LABELS: Record<number, { label: string; className: string }> = {
  1: { label: 'Easy', className: 'text-emerald-300 bg-emerald-500/10' },
  2: { label: 'Easy+', className: 'text-emerald-200 bg-emerald-500/10' },
  3: { label: 'Medium', className: 'text-yellow-300 bg-yellow-500/10' },
  4: { label: 'Hard-', className: 'text-orange-300 bg-orange-500/10' },
  5: { label: 'Hard', className: 'text-red-300 bg-red-500/10' },
};

export default function Problems() {
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [params] = useSearchParams();

  const difficulty = params.get('difficulty') ? Number(params.get('difficulty')) : undefined;
  const tagsParam = params.get('tags');
  const firstTag = tagsParam?.split(',')[0];

  useEffect(() => {
    problemsApi.list({ difficulty, tag: firstTag, limit: 200 }).then(setProblems);
  }, [difficulty, firstTag]);

  const filtered = useMemo(() => {
    if (!tagsParam) return problems;
    const tags = tagsParam.split(',').filter(Boolean);
    if (tags.length <= 1) return problems;
    return problems.filter((p) => tags.every((t) => p.tags.includes(t)));
  }, [problems, tagsParam]);

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

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Practice arena</h1>
        <p className="mt-1 text-sm text-white/60">Solve, earn XP, unlock badges.</p>
      </header>

      <div className="flex flex-col gap-6 lg:flex-row">
        <ProblemFilters
          totalByDifficulty={totals.byDifficulty}
          totalByTag={totals.byTag}
          availableTags={totals.tags}
        />

        <div className="flex-1 overflow-hidden rounded-2xl border border-white/5 bg-ink-800">
          <table className="w-full text-sm">
            <thead className="bg-ink-700 text-xs uppercase tracking-wider text-white/50">
              <tr>
                <th className="px-4 py-3 text-left">Title</th>
                <th className="px-4 py-3 text-left">Difficulty</th>
                <th className="px-4 py-3 text-left">Tags</th>
                <th className="px-4 py-3 text-right">XP</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id} className="border-t border-white/5 hover:bg-white/5">
                  <td className="px-4 py-3">
                    <Link to={`/problems/${p.id}`} className="text-white hover:text-brand-200">
                      {p.title}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-2 py-0.5 text-[10px] ${DIFFICULTY_LABELS[p.difficulty].className}`}
                    >
                      {DIFFICULTY_LABELS[p.difficulty].label}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-1">
                      {p.tags.slice(0, 3).map((t) => (
                        <span
                          key={t}
                          className="rounded-full bg-brand-600/10 px-2 py-0.5 text-[10px] text-brand-200"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-right text-xs text-brand-200">+{p.xp_reward}</td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-4 py-12 text-center text-sm text-white/50">
                    No problems match these filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
