import { Navigate, Route, Routes } from 'react-router-dom';
import { ReactElement, useEffect } from 'react';
import { useAuthStore } from './store/auth';

import Landing from './pages/Landing';
import Signup from './pages/Signup';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import TrackPage from './pages/Track';
import LessonPage from './pages/Lesson';
import Problems from './pages/Problems';
import ProblemDetail from './pages/ProblemDetail';
import Projects from './pages/Projects';
import Contests from './pages/Contests';
import Career from './pages/Career';
import Leaderboard from './pages/Leaderboard';
import Profile from './pages/Profile';
import AppShell from './components/AppShell';
import Toaster from './components/Toaster';

function Protected({ children }: { children: ReactElement }) {
  const token = useAuthStore((s) => s.accessToken);
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  const hydrate = useAuthStore((s) => s.hydrate);
  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <>
      <Toaster />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />

        <Route
          element={
            <Protected>
              <AppShell />
            </Protected>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/track/:trackId" element={<TrackPage />} />
          <Route path="/lesson/:lessonId" element={<LessonPage />} />
          <Route path="/problems" element={<Problems />} />
          <Route path="/problems/:problemId" element={<ProblemDetail />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/contests" element={<Contests />} />
          <Route path="/career" element={<Career />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/profile" element={<Profile />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
