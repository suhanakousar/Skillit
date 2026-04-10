import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/auth';
import { usersApi } from '../api/endpoints';
import type { Badge } from '../types';
import BadgeGrid from '../components/BadgeGrid';
import StreakCalendar from '../components/StreakCalendar';

export default function Profile() {
  const user = useAuthStore((s) => s.user);
  const [badges, setBadges] = useState<Badge[]>([]);

  useEffect(() => {
    usersApi.myBadges().then(setBadges);
  }, []);

  if (!user) return null;

  return (
    <div className="space-y-6">
      <header className="flex items-center gap-5">
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-brand-600 text-2xl font-bold text-white">
          {user.name
            .split(' ')
            .map((p) => p[0])
            .join('')
            .slice(0, 2)
            .toUpperCase()}
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">{user.name}</h1>
          <p className="text-sm text-white/60">
            Year {user.year} · {user.branch}
            {user.college ? ` · ${user.college}` : ''}
          </p>
          <div className="mt-2 flex gap-4 text-xs">
            <span className="text-brand-200">{user.xp_total} XP</span>
            <span className="text-orange-300">{user.streak_current}🔥 current</span>
            <span className="text-yellow-300">{user.streak_max} best</span>
          </div>
        </div>
      </header>

      <StreakCalendar current={user.streak_current} max={user.streak_max} />

      <section>
        <h2 className="mb-3 text-sm font-medium uppercase tracking-wider text-white/60">
          Badges earned ({badges.length})
        </h2>
        {badges.length > 0 ? (
          <BadgeGrid earned={badges} />
        ) : (
          <div className="rounded-xl border border-white/5 bg-ink-800 p-6 text-sm text-white/50">
            No badges yet — solve a problem to earn your first one.
          </div>
        )}
      </section>
    </div>
  );
}
