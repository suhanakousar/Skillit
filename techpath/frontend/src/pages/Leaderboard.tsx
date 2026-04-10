import { useEffect, useState } from 'react';
import { usersApi } from '../api/endpoints';
import type { LeaderboardEntry } from '../types';

export default function Leaderboard() {
  const [scope, setScope] = useState<'global' | 'college'>('global');
  const [rows, setRows] = useState<LeaderboardEntry[]>([]);

  useEffect(() => {
    usersApi.leaderboard(scope).then(setRows);
  }, [scope]);

  const medal = (rank: number) =>
    rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : `#${rank}`;

  return (
    <div className="space-y-6">
      <header className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Leaderboard</h1>
          <p className="mt-1 text-sm text-white/60">Top learners this week</p>
        </div>
        <div className="flex gap-1 rounded-full bg-ink-800 p-1 text-xs">
          {(['global', 'college'] as const).map((s) => (
            <button
              key={s}
              onClick={() => setScope(s)}
              className={`rounded-full px-3 py-1 ${
                scope === s ? 'bg-brand-600 text-white' : 'text-white/60'
              }`}
            >
              {s === 'global' ? 'All India' : 'My college'}
            </button>
          ))}
        </div>
      </header>

      <div className="overflow-hidden rounded-2xl border border-white/5 bg-ink-800">
        <table className="w-full text-sm">
          <thead className="bg-ink-700 text-xs uppercase tracking-wider text-white/50">
            <tr>
              <th className="px-4 py-3 text-left">Rank</th>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">College</th>
              <th className="px-4 py-3 text-right">XP</th>
              <th className="px-4 py-3 text-right">Streak</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.user_id} className="border-t border-white/5">
                <td className="px-4 py-3 font-mono text-white/80">{medal(r.rank)}</td>
                <td className="px-4 py-3 text-white">{r.name}</td>
                <td className="px-4 py-3 text-white/50">{r.college || '—'}</td>
                <td className="px-4 py-3 text-right text-brand-200">{r.xp_total}</td>
                <td className="px-4 py-3 text-right text-orange-300">{r.streak_current}🔥</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-12 text-center text-sm text-white/50">
                  No entries yet. Be the first!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
