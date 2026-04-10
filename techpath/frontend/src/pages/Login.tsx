import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from '../api/endpoints';
import { useAuthStore } from '../store/auth';
import { toast } from '../store/toast';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { access_token, refresh_token } = await authApi.login(email, password);
      setTokens(access_token, refresh_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const tryDemo = async () => {
    setError(null);
    setLoading(true);
    try {
      const { access_token, refresh_token } = await authApi.demoLogin();
      setTokens(access_token, refresh_token);
      toast.info('Demo account loaded', 'Explore freely — nothing is saved permanently');
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Demo not available');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-ink-900 p-6">
      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm space-y-4 rounded-2xl border border-white/10 bg-ink-800 p-8"
      >
        <div>
          <h1 className="text-xl font-semibold text-white">Welcome back</h1>
          <p className="mt-1 text-sm text-white/50">Sign in to your TechPath account</p>
        </div>

        <input
          type="email"
          placeholder="you@college.edu"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full rounded-lg border border-white/10 bg-ink-900 px-4 py-2.5 text-sm text-white outline-none focus:border-brand-500"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full rounded-lg border border-white/10 bg-ink-900 px-4 py-2.5 text-sm text-white outline-none focus:border-brand-500"
        />

        {error && <p className="text-xs text-red-300">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-brand-600 py-2.5 text-sm font-medium text-white hover:bg-brand-500 disabled:opacity-60"
        >
          {loading ? 'Signing in…' : 'Sign in'}
        </button>

        <div className="relative py-1 text-center">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-white/10" />
          </div>
          <span className="relative bg-ink-800 px-2 text-[10px] uppercase tracking-wider text-white/40">
            or
          </span>
        </div>

        <button
          type="button"
          onClick={tryDemo}
          disabled={loading}
          className="w-full rounded-lg border border-brand-500/40 bg-brand-600/10 py-2.5 text-sm font-medium text-brand-200 hover:bg-brand-600/20 disabled:opacity-60"
        >
          Try the demo account →
        </button>

        <p className="text-center text-xs text-white/50">
          No account?{' '}
          <Link to="/signup" className="text-brand-200 hover:underline">
            Create one
          </Link>
        </p>
      </form>
    </div>
  );
}
