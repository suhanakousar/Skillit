import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.redis_client import redis
from app.routers import (
    ai,
    auth,
    career,
    contests,
    lessons,
    problems,
    projects,
    roadmap,
    submissions,
    users,
)
from app.services.scheduler import scheduler_loop

logger = logging.getLogger("techpath")
logging.basicConfig(level=logging.INFO)


async def _bootstrap() -> None:
    """Create tables and seed starter content if the database is empty.

    Idempotent — running twice is safe. Skips everything if AUTO_BOOTSTRAP=false.
    """
    if not settings.auto_bootstrap:
        return

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as exc:
        logger.warning("auto_bootstrap: create_all failed: %s", exc)
        return

    try:
        from sqlalchemy import select

        from app.database import AsyncSessionLocal
        from app.models.track import Track

        async with AsyncSessionLocal() as db:
            existing = (await db.execute(select(Track).limit(1))).scalar_one_or_none()

        if existing is None:
            logger.info("auto_bootstrap: empty database detected — seeding")
            from app.seed import seed

            await seed()
            logger.info("auto_bootstrap: seed complete")
        else:
            logger.info("auto_bootstrap: tracks present — skipping seed")
    except Exception as exc:
        logger.exception("auto_bootstrap: seed failed: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _bootstrap()

    try:
        await redis.ping()
        logger.info("redis connected")
    except Exception as exc:
        logger.warning("redis unavailable: %s — leaderboards will use DB fallback", exc)

    scheduler_task = asyncio.create_task(scheduler_loop(60))

    try:
        yield
    finally:
        scheduler_task.cancel()
        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass
        try:
            await redis.close()
        except Exception:
            pass


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"service": settings.app_name, "status": "ok"}


@app.get("/health")
async def health():
    """Deeper health check: DB + Redis status."""
    from sqlalchemy import text

    status = {"status": "healthy", "db": "ok", "redis": "ok"}
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        status["status"] = "degraded"
        status["db"] = f"error: {exc}"
    try:
        await redis.ping()
    except Exception as exc:
        status["redis"] = f"error: {exc}"
    return status


prefix = settings.api_prefix
app.include_router(auth.router, prefix=f"{prefix}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{prefix}/users", tags=["users"])
app.include_router(roadmap.router, prefix=f"{prefix}/roadmap", tags=["roadmap"])
app.include_router(lessons.router, prefix=f"{prefix}/lessons", tags=["lessons"])
app.include_router(problems.router, prefix=f"{prefix}/problems", tags=["problems"])
app.include_router(submissions.router, prefix=f"{prefix}/submissions", tags=["submissions"])
app.include_router(projects.router, prefix=f"{prefix}/projects", tags=["projects"])
app.include_router(contests.router, prefix=f"{prefix}/contests", tags=["contests"])
app.include_router(career.router, prefix=f"{prefix}/career", tags=["career"])
app.include_router(ai.router, prefix=f"{prefix}/ai", tags=["ai"])
