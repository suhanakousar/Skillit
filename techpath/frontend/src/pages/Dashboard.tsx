import { useEffect, useState } from 'react';
import { roadmapApi, usersApi } from '../api/endpoints';
import type { Dashboard as DashboardPayload, RoadmapNode } from '../types';
import RoadmapTree from '../components/RoadmapTree';
import XPBar from '../components/XPBar';
import Skeleton, { CardSkeleton } from '../components/Skeleton';

export default function Dashboard() {
  const [data, setData] = useState<DashboardPayload | null>(null);
  const [nodes, setNodes] = useState<RoadmapNode[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    usersApi.dashboard().then(setData).catch((e) => setError(e?.message ?? 'Failed to load'));
    roadmapApi.get().then((r) => setNodes(r.nodes)).catch(() => setNodes([]));
  }, []);

  if (error) {
    return (
      <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-6 text-sm text-red-200">
        Could not load dashboard: {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-1/3" />
        <div className="grid gap-4 md:grid-cols-4">
          <CardSkeleton />
          <CardSkeleton />
          <CardSkeleton />
          <CardSkeleton />
        </div>
        <CardSkeleton />
      </div>
    );
  }

  const nextXpTarget = Math.max(1000, Math.ceil(data.user.xp_total / 1000) * 1000 + 1000);

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Hey {data.user.name.split(' ')[0]} 👋</h1>
        <p className="mt-1 text-sm text-white/60">{data.next_recommended_action}</p>
      </header>

      <div className="grid gap-4 md:grid-cols-4">
        <Stat label="XP total" value={data.user.xp_total} accent="text-brand-200" />
        <Stat label="Streak" value={`${data.user.streak_current}🔥`} accent="text-orange-300" />
        <Stat label="Problems solved" value={data.problems_solved} accent="text-emerald-300" />
        <Stat label="Badges" value={data.badges_earned} accent="text-yellow-300" />
      </div>

      <div className="rounded-2xl border border-white/5 bg-ink-800 p-5">
        <XPBar current={data.user.xp_total} target={nextXpTarget} label="Progress to next level" />
      </div>

      <section>
        <h2 className="mb-3 text-sm font-medium uppercase tracking-wider text-white/60">
          Your 4-year roadmap
        </h2>
        {nodes.length > 0 ? (
          <RoadmapTree nodes={nodes} />
        ) : (
          <div className="rounded-xl border border-white/5 bg-ink-800 p-6 text-sm text-white/50">
            Roadmap is being built. If this persists, the database may not be seeded yet.
          </div>
        )}
      </section>
    </div>
  );
}

function Stat({ label, value, accent }: { label: string; value: number | string; accent: string }) {
  return (
    <div className="rounded-2xl border border-white/5 bg-ink-800 p-5">
      <div className="text-xs uppercase tracking-wider text-white/50">{label}</div>
      <div className={`mt-1 text-3xl font-bold ${accent}`}>{value}</div>
    </div>
  );
}
