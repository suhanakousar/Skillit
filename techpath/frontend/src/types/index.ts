export type Branch = 'CSE' | 'AIDS' | 'AIML' | 'IoT' | 'ECE' | 'OTHER';
export type Goal = 'job' | 'gate' | 'startup' | 'research';
export type Language = 'python' | 'cpp' | 'java' | 'javascript' | 'c' | 'go';

export interface User {
  id: string;
  name: string;
  email: string;
  year: 1 | 2 | 3 | 4;
  branch: Branch;
  goal: Goal;
  preferred_language: Language;
  college: string | null;
  xp_total: number;
  streak_current: number;
  streak_max: number;
  last_active_date: string | null;
  created_at: string;
}

export interface Track {
  id: string;
  name: string;
  slug: string;
  domain: string;
  description: string | null;
  year_recommended: number;
  order_index: number;
  prerequisite_track_ids: string[];
  total_xp: number;
  estimated_hours: number;
  icon: string | null;
}

export interface RoadmapNode {
  id: string;
  year: number;
  domain: string;
  title: string;
  description: string | null;
  track_id: string | null;
  prerequisite_node_ids: string[];
  position_x: number;
  position_y: number;
  state: 'completed' | 'active' | 'unlocked' | 'locked';
}

export interface LessonSummary {
  id: string;
  title: string;
  type: 'story' | 'interactive' | 'codealong';
  xp_reward: number;
  order_index: number;
  duration_minutes: number;
}

export interface Lesson extends LessonSummary {
  track_id: string;
  content_json: {
    hook_story?: string;
    aha_moment?: string;
    concept_explained?: string;
    visual_description?: string;
    code_walkthrough?: { step: number; comment: string; code: string }[];
    quiz?: { question: string; options: string[]; correct: string; explanation: string }[];
    common_mistakes?: string[];
  };
}

export interface ProblemSummary {
  id: string;
  title: string;
  slug: string;
  difficulty: number;
  tags: string[];
  xp_reward: number;
}

export interface ProblemDetail extends ProblemSummary {
  description: string;
  starter_code_json: Record<string, string>;
  examples_json: Array<{ input: string; output: string }>;
  constraints_text: string | null;
  hints_json: Array<{ level: number; text: string }>;
}

export interface TestCaseResult {
  index: number;
  status: string;
  stdin?: string;
  stdout?: string;
  expected?: string;
  stderr?: string;
  runtime_ms?: number;
}

export interface SubmissionResult {
  id: string;
  status: 'accepted' | 'wrong_answer' | 'tle' | 'runtime_error' | 'compile_error' | 'pending';
  runtime_ms: number | null;
  memory_kb: number | null;
  percentile: number | null;
  xp_awarded: number;
  passed: number;
  total: number;
  compile_error?: string | null;
  failing_test?: TestCaseResult | null;
  test_results: TestCaseResult[];
  submitted_at: string;
}

export interface RunResult {
  status: string;
  compile_error?: string | null;
  results: TestCaseResult[];
}

export interface Project {
  id: string;
  title: string;
  slug: string;
  description: string;
  tech_stack: string[];
  milestones_json: Array<{ index: number; title: string; xp: number }>;
  year_recommended: number | null;
  xp_total: number;
}

export interface Badge {
  id: string;
  slug: string;
  name: string;
  description: string;
  icon: string | null;
  xp_bonus: number;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  name: string;
  college: string | null;
  xp_total: number;
  streak_current: number;
}

export interface Dashboard {
  user: User;
  tracks_in_progress: number;
  lessons_completed: number;
  problems_solved: number;
  badges_earned: number;
  next_recommended_action: string;
}

export interface ReadinessArea {
  area: string;
  required: number;
  current: number;
  gap: number;
  action: string;
}

export interface ReadinessResult {
  job_profile_id: string;
  company_name: string;
  role_title: string;
  overall_readiness: number;
  breakdown: ReadinessArea[];
  estimated_weeks_to_ready: number;
  next_milestone: string;
}

export interface JobProfile {
  id: string;
  slug: string;
  company_name: string;
  role_title: string;
  package_lpa: number | null;
  difficulty_level: number;
}
