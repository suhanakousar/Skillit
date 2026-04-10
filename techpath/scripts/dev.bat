@echo off
REM TechPath dev bootstrap for Windows. Requires: Docker Desktop, Python 3.12+, Node 20+.
setlocal enabledelayedexpansion

cd /d "%~dp0.."

if not exist .env (
  echo First run — copying infra\.env.example to .env
  copy infra\.env.example .env >nul
)

echo Starting Postgres + Redis
docker compose -f infra\docker-compose.yml up -d postgres redis

if not exist backend\.venv (
  echo Creating Python venv
  python -m venv backend\.venv
  call backend\.venv\Scripts\pip install --upgrade pip
  call backend\.venv\Scripts\pip install -r backend\requirements.txt
)

echo Seeding database (idempotent)
pushd backend
call .venv\Scripts\python -m app.seed
popd

if not exist frontend\node_modules (
  echo Installing frontend deps
  pushd frontend
  call npm install
  popd
)

echo.
echo Ready. Open two terminals:
echo   1) cd backend ^&^& .venv\Scripts\uvicorn app.main:app --reload --port 8000
echo   2) cd frontend ^&^& npm run dev
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000/docs
