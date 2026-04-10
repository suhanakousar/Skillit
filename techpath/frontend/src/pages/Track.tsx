import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { lessonsApi, roadmapApi } from '../api/endpoints';
import type { LessonSummary, Track as TrackType } from '../types';

export default function TrackPage() {
  const { trackId } = useParams<{ trackId: string }>();
  const [track, setTrack] = useState<TrackType | null>(null);
  const [lessons, setLessons] = useState<LessonSummary[]>([]);

  useEffect(() => {
    if (!trackId) return;
    roadmapApi.listTracks().then((ts) => setTrack(ts.find((t) => t.id === trackId) ?? null));
    lessonsApi.listByTrack(trackId).then(setLessons);
  }, [trackId]);

  if (!track) return <div className="text-white/50">Loading track…</div>;

  return (
    <div className="space-y-6">
      <header>
        <div className="text-xs uppercase tracking-wider text-brand-200">
          Year {track.year_recommended} · {track.domain}
        </div>
        <h1 className="mt-1 text-2xl font-bold text-white">{track.name}</h1>
        {track.description && <p className="mt-2 text-sm text-white/60">{track.description}</p>}
        <div className="mt-2 flex gap-4 text-xs text-white/50">
          <span>{track.total_xp} XP total</span>
          <span>{track.estimated_hours} hours</span>
        </div>
      </header>

      <section className="space-y-2">
        <h2 className="text-sm font-medium uppercase tracking-wider text-white/60">Lessons</h2>
        {lessons.length === 0 && (
          <div className="rounded-xl border border-white/5 bg-ink-800 p-6 text-center text-sm text-white/50">
            No lessons yet — check back soon.
          </div>
        )}
        {lessons.map((l, idx) => (
          <Link
            key={l.id}
            to={`/lesson/${l.id}`}
            className="flex items-center justify-between rounded-xl border border-white/5 bg-ink-800 p-4 hover:bg-ink-700"
          >
            <div>
              <div className="text-xs text-white/50">Lesson {idx + 1}</div>
              <div className="text-sm font-medium text-white">{l.title}</div>
            </div>
            <div className="text-xs text-brand-200">+{l.xp_reward} XP</div>
          </Link>
        ))}
      </section>
    </div>
  );
}
