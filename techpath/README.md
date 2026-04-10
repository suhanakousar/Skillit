# TechPath

A complete B.Tech CS learning platform for Indian engineering students. LeetCode-style practice, Duolingo-style story lessons, a 4-year visual roadmap, a projects lab, live contests, and a career-readiness layer — all in one.

## Stack

- **Frontend:** React 18 + Vite + TypeScript + Tailwind + Framer Motion + Zustand + Monaco Editor
- **Backend:** FastAPI (async) + SQLAlchemy 2.0 + Alembic
- **Database:** PostgreSQL 15 + Redis 7
- **Code execution:** Built-in local Python runner (zero config) — optional Judge0 for other languages
- **Auth:** JWT (access + refresh)
- **AI:** Anthropic Claude API (optional)

## Zero-config quick start

One command, no manual setup, no API keys required:

```bash
cd techpath
docker compose -f infra/docker-compose.yml up -d
```

That's it. The backend will:

1. Wait for Postgres and Redis to be healthy
2. Create all tables if they don't exist
3. Seed 20 tracks, 24 story lessons, 50+ problems, 13 projects, 20 badges, 6 job profiles, and a demo user
4. Start the scheduler and HTTP API

Open:

- **App:** http://localhost:3000
- **API docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

On the login page, click **"Try the demo account"** — you'll be signed in as `demo@techpath.dev` with 340 XP, a 5-day streak, 3 badges, 4 completed lessons, and 5 solved problems already populated. Or sign up fresh from the landing page.

## No Judge0? No problem.

Judge0 (the sandboxed code executor used by LeetCode) is complex to self-host. TechPath ships with an **in-process Python runner** as a fallback. When you submit a Python solution, the backend runs it in a subprocess with a 5-second timeout, compares stdout to expected output, and returns the same result shape Judge0 would.

> ⚠️ The local runner is fine for solo dev and demos. **Do not use it in production with untrusted code** — stand up real Judge0 for that.

To enable Judge0:

```bash
docker compose -f infra/docker-compose.yml --profile judge0 up -d
```

The backend auto-detects Judge0 at `$JUDGE0_URL` on every submission. If Judge0 is down, it silently falls back to the local runner.

## Native dev loop (hot reload)

```bash
# macOS / Linux
./scripts/dev.sh

# Windows
scripts\dev.bat
```

Then in two terminals:

```bash
cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev
```

## Config knobs

All via environment variables (see `infra/.env.example`):

| Variable | Default | Effect |
|---|---|---|
| `AUTO_BOOTSTRAP` | `true` | Create tables + seed on startup if DB is empty |
| `SEED_DEMO_USER` | `true` | Create the demo@techpath.dev account |
| `USE_LOCAL_RUNNER_FALLBACK` | `true` | Fall back to local runner when Judge0 is unavailable |
| `JUDGE0_URL` | `http://judge0:2358` | Where to find Judge0 (ignored if fallback kicks in) |
| `ANTHROPIC_API_KEY` | unset | Enables real Claude-powered hints and story lessons |
| `DEMO_EMAIL` / `DEMO_PASSWORD` | `demo@techpath.dev` / `techpath123` | Demo account credentials |

## What's in the seed

- **20 tracks** across 4 years and 6 domains (Programming, DSA, Web, Database, Systems, ML, DevOps, Cloud, Career)
- **24 story lessons** across 12 tracks — each has hook story, aha moment, code walkthrough, common mistakes, quiz
- **50+ problems** with real test cases covering arrays, strings, sliding window, binary search, trees, graphs, DP, stacks, linked lists, hard classics
- **13 projects** from CLI Todo to Full SaaS capstone
- **20 badges** with automatic condition evaluators
- **6 job profiles** (Amazon, Google, Microsoft, Infosys/TCS, Startup, ML Engineer)
- **Roadmap nodes** positioned across years for the visual tree
- **A live contest** seeded for demo
- **Demo user** with 340 XP, 5-day streak, 3 badges earned, 4 lessons completed, 5 problems solved

## Repo layout

```
techpath/
  backend/
    app/
      content/      Problems + lessons data modules
      models/       SQLAlchemy ORM models
      routers/      HTTP + WebSocket routes
      schemas/      Pydantic request/response schemas
      services/     XP, streaks, badges, scheduler, local runner, Judge0 client, Claude client, readiness
      main.py       FastAPI app + lifespan with auto-bootstrap
      seed.py       Idempotent seeder
    alembic/        Migrations (hand-written initial + env.py)
    tests/          pytest suite (auth, xp, streak, readiness, scheduler, judge0 normalize, local runner, security)
  frontend/
    src/
      pages/        13 routes (Landing, Signup, Login, Dashboard, Track, Lesson, Problems, ProblemDetail, Projects, Contests, Career, Leaderboard, Profile)
      components/   14 pieces (RoadmapTree, CodeEditor, HintChat, ProblemFilters, Toaster, Skeleton, AppShell, etc.)
      hooks/        useContestLeaderboard (WebSocket with polling fallback)
      store/        Zustand: auth, signup draft, toast
      api/          Typed Axios client + endpoints
  db/               Canonical schema.sql
  infra/            docker-compose, .env.example, nginx.conf
  content/          Curriculum JSONs (DSA, Full Stack, ML, System Design)
  scripts/          dev.sh, dev.bat, test.sh
```

## Tests

```bash
./scripts/test.sh
```

Runs the full backend suite against a real Postgres (created in-container on the fly) and type-checks the frontend. Pure unit tests (security, judge0 normalization, local runner) always run; DB tests skip cleanly if Postgres isn't reachable.

## Troubleshooting

- **App shows "Roadmap is being built":** The DB wasn't seeded. Check backend logs for `auto_bootstrap` messages. You can force it with `docker compose exec backend python -m app.seed`.
- **Demo login returns 404:** Either the seeder hasn't run yet, or `SEED_DEMO_USER=false`. Give the backend 30 seconds after first boot.
- **Submissions always show "compile error" for Java/C++:** The local runner defaults to Python only. Install the compilers in the backend image or enable Judge0 with `--profile judge0`.
- **AI hints say "offline":** Set `ANTHROPIC_API_KEY` in your `.env` and restart the backend.
- **"Connection refused" on the frontend:** Wait for the backend healthcheck to pass (`docker compose ps` shows `healthy`).

## Build phases

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| 1 | 1-2  | Auth + DB + onboarding |
| 2 | 3-4  | Story lessons + quiz |
| 3 | 5-6  | Practice arena + code runner |
| 4 | 7-8  | XP, badges, streaks |
| 5 | 9-10 | Projects + milestones |
| 6 | 11-12| Career readiness |
| 7 | 13-14| Contests + leaderboard |
| 8 | 15-16| Beta launch |
