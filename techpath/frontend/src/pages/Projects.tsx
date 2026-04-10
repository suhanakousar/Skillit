import { useEffect, useState } from 'react';
import { projectsApi } from '../api/endpoints';
import type { Project } from '../types';
import { toast } from '../store/toast';

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [yearFilter, setYearFilter] = useState<number | undefined>();

  useEffect(() => {
    projectsApi.list(yearFilter).then(setProjects);
  }, [yearFilter]);

  const start = async (p: Project) => {
    try {
      await projectsApi.start(p.id);
      toast.success(`${p.title} started`, 'Check your profile for milestones');
    } catch (err: any) {
      toast.error('Could not start project', err?.response?.data?.detail);
    }
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Projects lab</h1>
        <p className="mt-1 text-sm text-white/60">Ship real things. Build your portfolio.</p>
      </header>

      <div className="flex gap-2">
        <button
          onClick={() => setYearFilter(undefined)}
          className={`rounded-full px-3 py-1 text-xs ${yearFilter === undefined ? 'bg-brand-600' : 'bg-ink-800 text-white/60'}`}
        >
          All years
        </button>
        {[1, 2, 3, 4].map((y) => (
          <button
            key={y}
            onClick={() => setYearFilter(y)}
            className={`rounded-full px-3 py-1 text-xs ${yearFilter === y ? 'bg-brand-600' : 'bg-ink-800 text-white/60'}`}
          >
            Year {y}
          </button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((p) => (
          <div key={p.id} className="rounded-2xl border border-white/5 bg-ink-800 p-5">
            <div className="mb-1 text-[10px] uppercase tracking-wider text-brand-200">
              Year {p.year_recommended}
            </div>
            <h3 className="text-base font-semibold text-white">{p.title}</h3>
            <p className="mt-1 text-xs text-white/60">{p.description}</p>
            <div className="mt-3 flex flex-wrap gap-1">
              {p.tech_stack.map((s) => (
                <span key={s} className="rounded bg-ink-700 px-2 py-0.5 text-[10px] text-white/60">
                  {s}
                </span>
              ))}
            </div>
            <div className="mt-3 flex items-center justify-between text-xs">
              <span className="text-brand-200">+{p.xp_total} XP</span>
              <button
                onClick={() => start(p)}
                className="rounded bg-brand-600 px-3 py-1 font-medium text-white hover:bg-brand-500"
              >
                Start
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
