-- TechPath PostgreSQL schema
-- Requires: PostgreSQL 15+, pgcrypto extension for gen_random_uuid()

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================================================================
-- USERS & IDENTITY
-- =========================================================================

CREATE TABLE users (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              VARCHAR(120) NOT NULL,
    email             VARCHAR(255) NOT NULL UNIQUE,
    password_hash     VARCHAR(255) NOT NULL,
    year              SMALLINT NOT NULL CHECK (year BETWEEN 1 AND 4),
    branch            VARCHAR(20) NOT NULL CHECK (branch IN ('CSE','AIDS','AIML','IoT','ECE','OTHER')),
    goal              VARCHAR(20) NOT NULL CHECK (goal IN ('job','gate','startup','research')),
    preferred_language VARCHAR(20) NOT NULL DEFAULT 'python',
    college           VARCHAR(120),
    xp_total          INTEGER NOT NULL DEFAULT 0,
    streak_current    INTEGER NOT NULL DEFAULT 0,
    streak_max        INTEGER NOT NULL DEFAULT 0,
    last_active_date  DATE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_college ON users(college);
CREATE INDEX idx_users_xp ON users(xp_total DESC);

-- =========================================================================
-- TRACKS, LESSONS, PROGRESS
-- =========================================================================

CREATE TABLE tracks (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                   VARCHAR(120) NOT NULL,
    slug                   VARCHAR(120) NOT NULL UNIQUE,
    domain                 VARCHAR(40) NOT NULL,
    description            TEXT,
    year_recommended       SMALLINT NOT NULL CHECK (year_recommended BETWEEN 1 AND 4),
    order_index            INTEGER NOT NULL DEFAULT 0,
    prerequisite_track_ids UUID[] NOT NULL DEFAULT '{}',
    total_xp               INTEGER NOT NULL DEFAULT 0,
    estimated_hours        INTEGER NOT NULL DEFAULT 0,
    icon                   VARCHAR(40),
    created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tracks_domain ON tracks(domain);
CREATE INDEX idx_tracks_year ON tracks(year_recommended);

CREATE TABLE lessons (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    track_id         UUID NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    title            VARCHAR(200) NOT NULL,
    type             VARCHAR(20) NOT NULL CHECK (type IN ('story','interactive','codealong')),
    content_json     JSONB NOT NULL,
    xp_reward        INTEGER NOT NULL DEFAULT 10,
    order_index      INTEGER NOT NULL DEFAULT 0,
    duration_minutes INTEGER NOT NULL DEFAULT 10,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lessons_track ON lessons(track_id);

CREATE TABLE user_progress (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    track_id     UUID NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    lesson_id    UUID REFERENCES lessons(id) ON DELETE CASCADE,
    status       VARCHAR(20) NOT NULL DEFAULT 'not_started'
                 CHECK (status IN ('not_started','in_progress','completed')),
    score        INTEGER,
    completed_at TIMESTAMPTZ,
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, lesson_id)
);

CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_track ON user_progress(user_id, track_id);

-- =========================================================================
-- PROBLEMS & SUBMISSIONS
-- =========================================================================

CREATE TABLE problems (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    track_id          UUID REFERENCES tracks(id) ON DELETE SET NULL,
    title             VARCHAR(200) NOT NULL,
    slug              VARCHAR(200) NOT NULL UNIQUE,
    description       TEXT NOT NULL,
    difficulty        SMALLINT NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    tags              TEXT[] NOT NULL DEFAULT '{}',
    starter_code_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    test_cases_json   JSONB NOT NULL DEFAULT '[]'::jsonb,
    examples_json     JSONB NOT NULL DEFAULT '[]'::jsonb,
    constraints_text  TEXT,
    xp_reward         INTEGER NOT NULL DEFAULT 20,
    hints_json        JSONB NOT NULL DEFAULT '[]'::jsonb,
    solution_json     JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_problems_difficulty ON problems(difficulty);
CREATE INDEX idx_problems_tags ON problems USING GIN(tags);
CREATE INDEX idx_problems_track ON problems(track_id);

CREATE TABLE submissions (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id        UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
    language          VARCHAR(20) NOT NULL,
    code              TEXT NOT NULL,
    status            VARCHAR(20) NOT NULL
                      CHECK (status IN ('accepted','wrong_answer','tle','runtime_error','compile_error','pending')),
    runtime_ms        INTEGER,
    memory_kb         INTEGER,
    percentile        NUMERIC(5,2),
    test_results_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    submitted_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_submissions_user_problem ON submissions(user_id, problem_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_submitted ON submissions(submitted_at DESC);

-- =========================================================================
-- PROJECTS
-- =========================================================================

CREATE TABLE projects (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    track_id          UUID REFERENCES tracks(id) ON DELETE SET NULL,
    title             VARCHAR(200) NOT NULL,
    slug              VARCHAR(200) NOT NULL UNIQUE,
    description       TEXT NOT NULL,
    tech_stack        TEXT[] NOT NULL DEFAULT '{}',
    milestones_json   JSONB NOT NULL DEFAULT '[]'::jsonb,
    year_recommended  SMALLINT CHECK (year_recommended BETWEEN 1 AND 4),
    xp_total          INTEGER NOT NULL DEFAULT 100,
    repo_template_url VARCHAR(500),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_projects_year ON projects(year_recommended);

CREATE TABLE user_projects (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id               UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id            UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    status                VARCHAR(20) NOT NULL DEFAULT 'in_progress'
                          CHECK (status IN ('in_progress','submitted','reviewed','completed')),
    milestones_completed  JSONB NOT NULL DEFAULT '[]'::jsonb,
    github_url            VARCHAR(500),
    live_url              VARCHAR(500),
    submitted_at          TIMESTAMPTZ,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, project_id)
);

-- =========================================================================
-- BADGES
-- =========================================================================

CREATE TABLE badges (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug           VARCHAR(60) NOT NULL UNIQUE,
    name           VARCHAR(120) NOT NULL,
    description    TEXT NOT NULL,
    icon           VARCHAR(60),
    condition_json JSONB NOT NULL,
    xp_bonus       INTEGER NOT NULL DEFAULT 0,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_badges (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id  UUID NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
    earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, badge_id)
);

CREATE INDEX idx_user_badges_user ON user_badges(user_id);

-- =========================================================================
-- CONTESTS
-- =========================================================================

CREATE TABLE contests (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    start_time  TIMESTAMPTZ NOT NULL,
    end_time    TIMESTAMPTZ NOT NULL,
    problem_ids UUID[] NOT NULL DEFAULT '{}',
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contests_start ON contests(start_time DESC);

CREATE TABLE contest_submissions (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contest_id        UUID NOT NULL REFERENCES contests(id) ON DELETE CASCADE,
    user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id        UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
    submission_id     UUID REFERENCES submissions(id) ON DELETE SET NULL,
    points            INTEGER NOT NULL DEFAULT 0,
    time_taken_seconds INTEGER NOT NULL DEFAULT 0,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contest_subs_contest ON contest_submissions(contest_id, points DESC);

-- =========================================================================
-- CAREER / JOB READINESS
-- =========================================================================

CREATE TABLE job_profiles (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug             VARCHAR(80) NOT NULL UNIQUE,
    company_name     VARCHAR(120) NOT NULL,
    role_title       VARCHAR(120) NOT NULL,
    package_lpa      NUMERIC(6,2),
    required_skills  JSONB NOT NULL DEFAULT '[]'::jsonb,
    required_tracks  UUID[] NOT NULL DEFAULT '{}',
    difficulty_level SMALLINT NOT NULL CHECK (difficulty_level BETWEEN 1 AND 5),
    application_url  VARCHAR(500),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_job_readiness (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_profile_id     UUID NOT NULL REFERENCES job_profiles(id) ON DELETE CASCADE,
    readiness_percent  SMALLINT NOT NULL DEFAULT 0 CHECK (readiness_percent BETWEEN 0 AND 100),
    gap_areas_json     JSONB NOT NULL DEFAULT '[]'::jsonb,
    last_calculated    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, job_profile_id)
);

CREATE TABLE certifications (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name               VARCHAR(200) NOT NULL,
    provider           VARCHAR(40) NOT NULL,
    related_track_ids  UUID[] NOT NULL DEFAULT '{}',
    difficulty         SMALLINT NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    exam_url           VARCHAR(500),
    tips_json          JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE TABLE user_certifications (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    cert_id        UUID NOT NULL REFERENCES certifications(id) ON DELETE CASCADE,
    status         VARCHAR(20) NOT NULL DEFAULT 'planned'
                   CHECK (status IN ('planned','in_progress','passed')),
    passed_at      TIMESTAMPTZ,
    credential_url VARCHAR(500),
    UNIQUE (user_id, cert_id)
);

-- =========================================================================
-- ROADMAP VISUAL
-- =========================================================================

CREATE TABLE roadmap_nodes (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    year                    SMALLINT NOT NULL CHECK (year BETWEEN 1 AND 4),
    domain                  VARCHAR(40) NOT NULL,
    title                   VARCHAR(120) NOT NULL,
    description             TEXT,
    prerequisite_node_ids   UUID[] NOT NULL DEFAULT '{}',
    track_id                UUID REFERENCES tracks(id) ON DELETE SET NULL,
    position_x              INTEGER NOT NULL DEFAULT 0,
    position_y              INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_roadmap_year ON roadmap_nodes(year);
