import { useCallback, useEffect, useState } from 'react';
import { contestsApi } from '../api/endpoints';
import ContestTimer from '../components/ContestTimer';
import { useContestLeaderboard } from '../hooks/useContestLeaderboard';

interface Contest {
  id: string;
  title: string;
  description: string | null;
  start_time: string;
  end_time: string;
  is_active: boolean;
}

export default function Contests() {
  const [active, setActive] = useState<Contest | null>(null);
  const [contests, setContests] = useState<Contest[]>([]);

  useEffect(() => {
    contestsApi.active().then(setActive);
    contestsApi.list().then(setContests);
  }, []);

  const pollFallback = useCallback(async () => {
    if (!active) return [];
    return contestsApi.leaderboard(active.id);
  }, [active]);

  const board = useContestLeaderboard(active?.id, pollFallback);

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Contests</h1>
        <p className="mt-1 text-sm text-white/60">Saturdays 8PM IST · 90 minutes · 3 problems</p>
      </header>

      {active ? (
        <div className="rounded-2xl border border-brand-500/40 bg-brand-600/10 p-6">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
                <div className="text-xs uppercase tracking-wider text-brand-200">Live now</div>
              </div>
              <h2 className="mt-1 text-xl font-bold text-white">{active.title}</h2>
              <p className="mt-1 text-sm text-white/60">{active.description}</p>
            </div>
            <ContestTimer endTime={active.end_time} />
          </div>

          <div className="mt-6">
            <h3 className="mb-2 text-xs font-medium uppercase tracking-wider text-white/60">
              Live leaderboard
            </h3>
            <div className="space-y-1">
              {board.map((row) => (
                <div
                  key={row.user_id}
                  className="flex items-center justify-between rounded bg-ink-800 px-3 py-2 text-xs"
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 font-mono text-brand-200">#{row.rank}</span>
                    <span className="text-white">{row.name}</span>
                    {row.college && <span className="text-white/40">{row.college}</span>}
                  </div>
                  <span className="font-mono text-brand-100">{row.points} pts</span>
                </div>
              ))}
              {board.length === 0 && (
                <p className="text-xs text-white/50">No submissions yet — be the first!</p>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="rounded-2xl border border-white/5 bg-ink-800 p-6 text-sm text-white/60">
          No active contest right now. Next one drops Saturday 8PM IST.
        </div>
      )}

      <section>
        <h2 className="mb-3 text-sm font-medium uppercase tracking-wider text-white/60">
          Past contests
        </h2>
        <div className="space-y-2">
          {contests.map((c) => (
            <div
              key={c.id}
              className="flex items-center justify-between rounded-xl border border-white/5 bg-ink-800 p-4"
            >
              <div>
                <div className="text-sm font-medium text-white">{c.title}</div>
                <div className="text-xs text-white/50">
                  {new Date(c.start_time).toLocaleString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
