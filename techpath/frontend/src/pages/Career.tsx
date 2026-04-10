import { useEffect, useState } from 'react';
import { careerApi } from '../api/endpoints';
import type { JobProfile, ReadinessResult } from '../types';
import JobReadinessBar from '../components/JobReadinessBar';

export default function Career() {
  const [jobs, setJobs] = useState<JobProfile[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [readiness, setReadiness] = useState<ReadinessResult | null>(null);

  useEffect(() => {
    careerApi.jobs().then((js) => {
      setJobs(js);
      if (js[0]) setSelected(js[0].id);
    });
  }, []);

  useEffect(() => {
    if (!selected) return;
    careerApi.readiness(selected).then(setReadiness);
  }, [selected]);

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Career intelligence</h1>
        <p className="mt-1 text-sm text-white/60">
          See your exact gap to your dream job — and what to do next.
        </p>
      </header>

      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <h2 className="mb-3 text-xs font-medium uppercase tracking-wider text-white/60">
            Pick a target role
          </h2>
          <div className="space-y-2">
            {jobs.map((j) => (
              <button
                key={j.id}
                onClick={() => setSelected(j.id)}
                className={`w-full rounded-xl border p-4 text-left transition ${
                  selected === j.id
                    ? 'border-brand-500 bg-brand-600/10'
                    : 'border-white/5 bg-ink-800 hover:bg-ink-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-white">{j.company_name}</div>
                    <div className="text-xs text-white/50">{j.role_title}</div>
                  </div>
                  {j.package_lpa && (
                    <div className="text-xs font-medium text-emerald-300">
                      ₹{j.package_lpa}L
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div>
          {readiness ? (
            <>
              <JobReadinessBar
                overall={readiness.overall_readiness}
                breakdown={readiness.breakdown}
              />
              <div className="mt-4 rounded-xl border border-brand-500/30 bg-brand-600/10 p-4 text-xs text-white">
                <div className="mb-1 font-medium">Next milestone</div>
                <div className="text-brand-100">{readiness.next_milestone}</div>
                <div className="mt-2 text-white/60">
                  ≈ {readiness.estimated_weeks_to_ready} weeks to ready
                </div>
              </div>
            </>
          ) : (
            <div className="rounded-xl border border-white/5 bg-ink-800 p-6 text-sm text-white/50">
              Select a role to see your readiness
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
