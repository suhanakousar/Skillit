import { api } from './client';
import type {
  Badge,
  Dashboard,
  JobProfile,
  LeaderboardEntry,
  Lesson,
  LessonSummary,
  ProblemDetail,
  ProblemSummary,
  Project,
  ReadinessResult,
  RoadmapNode,
  SubmissionResult,
  Track,
  User,
} from '../types';

export interface SignupPayload {
  name: string;
  email: string;
  password: string;
  year: number;
  branch: string;
  goal: string;
  preferred_language: string;
  college?: string | null;
}

export const authApi = {
  signup: (data: SignupPayload) =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/signup', data).then((r) => r.data),
  login: (email: string, password: string) =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/login', { email, password }).then((r) => r.data),
  demoLogin: () =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/demo-login').then((r) => r.data),
  me: () => api.get<User>('/auth/me').then((r) => r.data),
};

export const usersApi = {
  dashboard: () => api.get<Dashboard>('/users/dashboard').then((r) => r.data),
  leaderboard: (scope: 'global' | 'college' = 'global') =>
    api.get<LeaderboardEntry[]>('/users/leaderboard', { params: { scope } }).then((r) => r.data),
  myBadges: () => api.get<Badge[]>('/users/me/badges').then((r) => r.data),
};

export const roadmapApi = {
  get: () => api.get<{ nodes: RoadmapNode[] }>('/roadmap').then((r) => r.data),
  listTracks: () => api.get<Track[]>('/roadmap/tracks').then((r) => r.data),
};

export const lessonsApi = {
  listByTrack: (trackId: string) =>
    api.get<LessonSummary[]>(`/lessons/track/${trackId}`).then((r) => r.data),
  get: (lessonId: string) => api.get<Lesson>(`/lessons/${lessonId}`).then((r) => r.data),
  complete: (lessonId: string) =>
    api.post<{ xp_awarded: number; streak: { streak_current: number }; new_badges: { slug: string; name: string }[] }>(
      `/lessons/${lessonId}/complete`,
    ).then((r) => r.data),
};

export const problemsApi = {
  list: (params: { difficulty?: number; tag?: string; limit?: number } = {}) =>
    api.get<ProblemSummary[]>('/problems', { params }).then((r) => r.data),
  get: (id: string) => api.get<ProblemDetail>(`/problems/${id}`).then((r) => r.data),
};

export const submissionsApi = {
  submit: (problem_id: string, language: string, code: string) =>
    api.post<SubmissionResult>('/submissions', { problem_id, language, code }).then((r) => r.data),
  history: (problem_id: string) =>
    api.get(`/submissions/me/problem/${problem_id}`).then((r) => r.data),
};

export const projectsApi = {
  list: (year?: number) => api.get<Project[]>('/projects', { params: { year } }).then((r) => r.data),
  start: (id: string) => api.post(`/projects/${id}/start`).then((r) => r.data),
  updateMilestone: (id: string, milestoneIndex: number, xpReward = 30) =>
    api.post(`/projects/${id}/milestone`, { milestone_index: milestoneIndex, completed: true, xp_reward: xpReward }).then((r) => r.data),
  submit: (id: string, githubUrl: string, liveUrl?: string) =>
    api.post(`/projects/${id}/submit`, { github_url: githubUrl, live_url: liveUrl }).then((r) => r.data),
};

export const contestsApi = {
  list: () => api.get('/contests').then((r) => r.data),
  active: () => api.get('/contests/active').then((r) => r.data),
  leaderboard: (id: string) => api.get(`/contests/${id}/leaderboard`).then((r) => r.data),
};

export const careerApi = {
  jobs: () => api.get<JobProfile[]>('/career/jobs').then((r) => r.data),
  readiness: (jobId: string) =>
    api.get<ReadinessResult>(`/career/readiness/${jobId}`).then((r) => r.data),
  readinessAll: () => api.get('/career/readiness').then((r) => r.data),
};

export const aiApi = {
  hint: (problem_id: string, hint_level: number, user_code?: string) =>
    api.post('/ai/hint', { problem_id, hint_level, user_code }).then((r) => r.data),
  review: (code: string, language: string, problem_id?: string) =>
    api.post('/ai/review', { code, language, problem_id }).then((r) => r.data),
};
