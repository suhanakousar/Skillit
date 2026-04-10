import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { authApi } from '../api/endpoints';
import { useAuthStore } from '../store/auth';
import { useSignupDraft } from '../store/signup';
import type { Branch, Goal, Language } from '../types';

const BRANCHES: { code: Branch; label: string; desc: string }[] = [
  { code: 'CSE', label: 'CSE', desc: 'Classic CS' },
  { code: 'AIDS', label: 'AI & DS', desc: 'AI + Data' },
  { code: 'AIML', label: 'AI & ML', desc: 'ML focused' },
  { code: 'IoT', label: 'IoT', desc: 'Embedded + Cloud' },
  { code: 'ECE', label: 'ECE', desc: 'Electronics' },
  { code: 'OTHER', label: 'Other', desc: 'Something else' },
];

const GOALS: { code: Goal; label: string; unlocks: string }[] = [
  { code: 'job', label: 'Get a product job', unlocks: 'DSA + System design + Projects + Mock interviews' },
  { code: 'gate', label: 'Crack GATE', unlocks: 'OS + Networks + DBMS + Aptitude + Past papers' },
  { code: 'startup', label: 'Build startups', unlocks: 'Full stack + Deployment + Product + MVP kit' },
  { code: 'research', label: 'Research / MS abroad', unlocks: 'ML + Math + Reading papers + SOP help' },
];

const LANGS: { code: Language; label: string; emoji: string; use: string }[] = [
  { code: 'python', label: 'Python', emoji: '🐍', use: 'Beginner-friendly, ML, DSA' },
  { code: 'cpp', label: 'C++', emoji: '⚡', use: 'Fast, competitive programming' },
  { code: 'java', label: 'Java', emoji: '☕', use: 'Enterprise, Android, placements' },
  { code: 'javascript', label: 'JavaScript', emoji: '✨', use: 'Web, Node.js, full stack' },
];

export default function Signup() {
  const draft = useSignupDraft();
  const navigate = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canProceed = () => {
    if (draft.step === 1) {
      return draft.name.length >= 2 && draft.email.includes('@') && draft.password.length >= 8;
    }
    if (draft.step === 2) return draft.year !== null && draft.branch !== null;
    if (draft.step === 3) return draft.goal !== null;
    if (draft.step === 4) return !!draft.preferred_language;
    return false;
  };

  const finish = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const { access_token, refresh_token } = await authApi.signup({
        name: draft.name,
        email: draft.email,
        password: draft.password,
        year: draft.year!,
        branch: draft.branch!,
        goal: draft.goal!,
        preferred_language: draft.preferred_language,
        college: draft.college || undefined,
      });
      setTokens(access_token, refresh_token);
      draft.reset();
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Signup failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-ink-900 p-6">
      <div className="w-full max-w-lg rounded-2xl border border-white/10 bg-ink-800 p-8">
        <div className="mb-6 flex items-center justify-center gap-2">
          {[1, 2, 3, 4].map((s) => (
            <div
              key={s}
              className={`h-1.5 w-8 rounded-full transition ${
                s <= draft.step ? 'bg-brand-500' : 'bg-white/10'
              }`}
            />
          ))}
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={draft.step}
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -30 }}
            transition={{ duration: 0.2 }}
            className="space-y-4"
          >
            {draft.step === 1 && (
              <>
                <h2 className="text-xl font-semibold text-white">Create your account</h2>
                <input
                  type="text"
                  placeholder="Full name"
                  value={draft.name}
                  onChange={(e) => draft.setField('name', e.target.value)}
                  className="w-full rounded-lg border border-white/10 bg-ink-900 px-4 py-2.5 text-sm text-white outline-none focus:border-brand-500"
                />
                <input
                  type="email"
                  placeholder="Email"
                  value={draft.email}
                  onChange={(e) => draft.setField('email', e.target.value)}
                  className="w-full rounded-lg border border-white/10 bg-ink-900 px-4 py-2.5 text-sm text-white outline-none focus:border-brand-500"
                />
                <input
                  type="password"
                  placeholder="Password (min 8 chars)"
                  value={draft.password}
                  onChange={(e) => draft.setField('password', e.target.value)}
                  className="w-full rounded-lg border border-white/10 bg-ink-900 px-4 py-2.5 text-sm text-white outline-none focus:border-brand-500"
                />
                <input
                  type="text"
                  placeholder="College (optional — e.g. KL University)"
                  value={draft.college}
                  onChange={(e) => draft.setField('college', e.target.value)}
                  className="w-full rounded-lg border border-white/10 bg-ink-900 px-4 py-2.5 text-sm text-white outline-none focus:border-brand-500"
                />
              </>
            )}

            {draft.step === 2 && (
              <>
                <h2 className="text-xl font-semibold text-white">Your academic profile</h2>
                <div>
                  <p className="mb-2 text-xs text-white/50">Which year are you in?</p>
                  <div className="flex gap-2">
                    {([1, 2, 3, 4] as const).map((y) => (
                      <button
                        key={y}
                        onClick={() => draft.setField('year', y)}
                        className={`flex-1 rounded-lg border px-4 py-2 text-sm transition ${
                          draft.year === y
                            ? 'border-brand-500 bg-brand-600/20 text-white'
                            : 'border-white/10 text-white/60 hover:bg-white/5'
                        }`}
                      >
                        {y === 1 ? '1st' : y === 2 ? '2nd' : y === 3 ? '3rd' : '4th'}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="mb-2 text-xs text-white/50">Branch</p>
                  <div className="grid grid-cols-3 gap-2">
                    {BRANCHES.map((b) => (
                      <button
                        key={b.code}
                        onClick={() => draft.setField('branch', b.code)}
                        className={`rounded-lg border p-3 text-left transition ${
                          draft.branch === b.code
                            ? 'border-brand-500 bg-brand-600/20'
                            : 'border-white/10 hover:bg-white/5'
                        }`}
                      >
                        <div className="text-sm font-medium text-white">{b.label}</div>
                        <div className="text-[10px] text-white/50">{b.desc}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}

            {draft.step === 3 && (
              <>
                <h2 className="text-xl font-semibold text-white">What's your goal?</h2>
                <div className="space-y-2">
                  {GOALS.map((g) => (
                    <button
                      key={g.code}
                      onClick={() => draft.setField('goal', g.code)}
                      className={`w-full rounded-lg border p-4 text-left transition ${
                        draft.goal === g.code
                          ? 'border-brand-500 bg-brand-600/20'
                          : 'border-white/10 hover:bg-white/5'
                      }`}
                    >
                      <div className="text-sm font-medium text-white">{g.label}</div>
                      <div className="mt-1 text-xs text-white/50">Unlocks: {g.unlocks}</div>
                    </button>
                  ))}
                </div>
              </>
            )}

            {draft.step === 4 && (
              <>
                <h2 className="text-xl font-semibold text-white">Pick your language</h2>
                <div className="grid grid-cols-2 gap-2">
                  {LANGS.map((l) => (
                    <button
                      key={l.code}
                      onClick={() => draft.setField('preferred_language', l.code)}
                      className={`rounded-lg border p-4 text-left transition ${
                        draft.preferred_language === l.code
                          ? 'border-brand-500 bg-brand-600/20'
                          : 'border-white/10 hover:bg-white/5'
                      }`}
                    >
                      <div className="text-xl">{l.emoji}</div>
                      <div className="mt-1 text-sm font-medium text-white">{l.label}</div>
                      <div className="text-[10px] text-white/50">{l.use}</div>
                    </button>
                  ))}
                </div>
              </>
            )}
          </motion.div>
        </AnimatePresence>

        {error && <p className="mt-3 text-xs text-red-300">{error}</p>}

        <div className="mt-6 flex gap-2">
          {draft.step > 1 && (
            <button
              onClick={draft.prev}
              className="rounded-lg border border-white/10 px-4 py-2 text-xs text-white/70 hover:bg-white/5"
            >
              ← Back
            </button>
          )}
          {draft.step < 4 ? (
            <button
              onClick={draft.next}
              disabled={!canProceed()}
              className="ml-auto rounded-lg bg-brand-600 px-6 py-2 text-xs font-medium text-white hover:bg-brand-500 disabled:opacity-50"
            >
              Continue →
            </button>
          ) : (
            <button
              onClick={finish}
              disabled={!canProceed() || submitting}
              className="ml-auto rounded-lg bg-brand-600 px-6 py-2 text-xs font-medium text-white hover:bg-brand-500 disabled:opacity-50"
            >
              {submitting ? 'Building your roadmap…' : 'Generate my roadmap →'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
