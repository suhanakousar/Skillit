import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuthStore } from '../store/auth';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '🏠' },
  { to: '/problems', label: 'Problems', icon: '⚡' },
  { to: '/projects', label: 'Projects', icon: '🛠️' },
  { to: '/contests', label: 'Contests', icon: '🏆' },
  { to: '/career', label: 'Career', icon: '🎯' },
  { to: '/leaderboard', label: 'Leaderboard', icon: '📊' },
  { to: '/profile', label: 'Profile', icon: '👤' },
];

export default function AppShell() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen bg-ink-900 text-white">
      <aside className="hidden md:flex md:w-60 flex-col border-r border-white/5 bg-ink-800 p-4 sticky top-0 h-screen">
        <div className="mb-8 px-2">
          <div className="text-xl font-bold text-brand-200">TechPath</div>
          <div className="text-xs text-white/50">From curious to hired</div>
        </div>
        <nav className="flex flex-col gap-1 flex-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition ${
                  isActive
                    ? 'bg-brand-600/20 text-white border border-brand-500/30'
                    : 'text-white/60 hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        {user && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 rounded-lg bg-ink-700 p-3 text-xs"
          >
            <div className="font-semibold text-white">{user.name}</div>
            <div className="text-white/50">{user.college || 'No college set'}</div>
            <div className="mt-2 flex items-center justify-between text-[11px]">
              <span className="text-brand-200">{user.xp_total} XP</span>
              <span className="text-orange-300">{user.streak_current}🔥</span>
            </div>
            <button
              onClick={() => {
                logout();
                navigate('/login');
              }}
              className="mt-3 w-full rounded bg-white/5 py-1 text-[11px] text-white/60 hover:bg-white/10"
            >
              Log out
            </button>
          </motion.div>
        )}
      </aside>

      <main className="flex-1 min-w-0">
        <div className="mx-auto max-w-7xl p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
