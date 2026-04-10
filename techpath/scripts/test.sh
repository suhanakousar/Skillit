#!/usr/bin/env bash
# Run backend + frontend tests. Spins up a Postgres test DB if not already running.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "→ Ensuring postgres is running"
docker compose -f infra/docker-compose.yml up -d postgres

echo "→ Creating techpath_test DB if missing"
docker compose -f infra/docker-compose.yml exec -T postgres \
  psql -U techpath -d techpath -tc "SELECT 1 FROM pg_database WHERE datname='techpath_test'" | grep -q 1 \
  || docker compose -f infra/docker-compose.yml exec -T postgres createdb -U techpath techpath_test

echo "→ Running backend tests"
(cd backend && \
  TEST_DATABASE_URL=postgresql+asyncpg://techpath:techpath@localhost:5432/techpath_test \
  .venv/bin/pytest)

echo "→ Running frontend type-check"
(cd frontend && npx tsc -b --noEmit)

echo "All checks passed."
