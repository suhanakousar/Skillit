import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { authApi } from '../api/endpoints';
import { useAuthStore } from '../store/auth';
import { toast } from '../store/toast';

export default function Landing() {
  const navigate = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);
  const [loading, setLoading] = useState(false);

  const tryDemo = async () => {
    setLoading(true);
    try {
      const { access_token, refresh_token } = await authApi.demoLogin();
      setTokens(access_token, refresh_token);
      toast.info('Demo account loaded', 'Explore freely');
      navigate('/dashboard');
    } catch (err: any) {
      toast.error('Demo not available', err?.response?.data?.detail ?? 'Try signing up instead');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-ink-900 text-white">
      <header className="mx-auto flex max-w-6xl items-center justify-between p-6">
        <div className="text-xl font-bold text-brand-200">TechPath</div>
        <nav className="flex gap-4 text-sm">
          <Link to="/login" className="text-white/70 hover:text-white">
            Log in
          </Link>
          <Link
            to="/signup"
            className="rounded-lg bg-brand-600 px-4 py-2 font-medium hover:bg-brand-500"
          >
            Get started
          </Link>
        </nav>
      </header>

      <main className="mx-auto max-w-6xl px-6 pt-12 pb-24">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl"
        >
          <div className="mb-3 inline-block rounded-full bg-brand-600/20 px-3 py-1 text-xs text-brand-200 border border-brand-500/30">
            Built for Indian B.Tech students
          </div>
          <h1 className="text-5xl font-bold leading-tight md:text-6xl">
            From curious to hired — <span className="text-brand-200">one story at a time.</span>
          </h1>
          <p className="mt-6 text-lg text-white/70">
            TechPath guides you from Year 1 basics to placement-ready in Year 4. Story-driven lessons,
            LeetCode-style practice, real projects, weekly contests, and a career readiness dashboard
            that tells you exactly what to learn next.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              to="/signup"
              className="rounded-xl bg-brand-600 px-6 py-3 text-sm font-medium hover:bg-brand-500"
            >
              Generate my roadmap →
            </Link>
            <button
              onClick={tryDemo}
              disabled={loading}
              className="rounded-xl border border-brand-500/40 bg-brand-600/10 px-6 py-3 text-sm font-medium text-brand-200 hover:bg-brand-600/20 disabled:opacity-50"
            >
              {loading ? 'Loading demo…' : 'Try the demo account'}
            </button>
            <Link
              to="/login"
              className="rounded-xl border border-white/20 px-6 py-3 text-sm font-medium hover:bg-white/5"
            >
              I already have an account
            </Link>
          </div>
        </motion.div>

        <div className="mt-20 grid gap-4 md:grid-cols-3">
          {[
            { title: 'Story lessons', desc: 'Every concept taught as a narrative, not a textbook dump.' },
            { title: 'Smart roadmap', desc: 'Year-aware, branch-aware, goal-aware. Unlocks as you level up.' },
            { title: 'Job-readiness meter', desc: 'See your gap to Amazon, Google, Infosys — and exactly how to close it.' },
          ].map((f) => (
            <div key={f.title} className="rounded-2xl border border-white/10 bg-ink-800 p-6">
              <div className="text-lg font-semibold">{f.title}</div>
              <p className="mt-2 text-sm text-white/60">{f.desc}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
