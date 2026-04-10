#!/usr/bin/env bash
# TechPath dev bootstrap — starts Postgres + Redis in Docker, runs backend and
# frontend natively so hot-reload is fast. Requires: docker, python3.12+, node 20+.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "First run — copying infra/.env.example to .env"
  cp infra/.env.example .env
fi

echo "→ Starting Postgres + Redis"
docker compose -f infra/docker-compose.yml up -d postgres redis

if [ ! -d backend/.venv ]; then
  echo "→ Creating Python venv"
  python3 -m venv backend/.venv
  backend/.venv/bin/pip install --upgrade pip
  backend/.venv/bin/pip install -r backend/requirements.txt
fi

echo "→ Seeding database (idempotent)"
(cd backend && .venv/bin/python -m app.seed) || echo "seed skipped (already present or postgres not ready)"

if [ ! -d frontend/node_modules ]; then
  echo "→ Installing frontend deps"
  (cd frontend && npm install)
fi

echo ""
echo "Ready. Open two terminals:"
echo "  1) cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000"
echo "  2) cd frontend && npm run dev"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000/docs"
