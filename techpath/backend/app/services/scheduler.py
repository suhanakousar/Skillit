"""Lightweight background scheduler for periodic tasks.

Runs inside the FastAPI lifespan — no Celery needed for simple periodic jobs
like closing expired contests and awarding contest-winner badges.
"""
import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.contest import Contest, ContestSubmission
from app.models.user import User
from app.redis_client import redis
from app.services.badges import check_badges
from app.services.xp import award_xp

logger = logging.getLogger(__name__)

CONTEST_WIN_XP = 500


async def close_expired_contests() -> int:
    """Mark contests whose end time has passed as inactive and award winners.

    Returns the number of contests closed.
    """
    closed = 0
    async with AsyncSessionLocal() as db:
        now = datetime.now(timezone.utc)
        stmt = select(Contest).where(Contest.is_active.is_(True), Contest.end_time < now)
        expired = (await db.execute(stmt)).scalars().all()

        for contest in expired:
            try:
                top_user_ids: list[str] = []
                try:
                    raw = await redis.zrevrange(
                        f"contest:{contest.id}:leaderboard", 0, 0, withscores=True
                    )
                    top_user_ids = [uid for uid, _ in raw]
                except Exception:
                    pass

                if not top_user_ids:
                    sub_stmt = (
                        select(ContestSubmission.user_id)
                        .where(ContestSubmission.contest_id == contest.id)
                        .order_by(ContestSubmission.points.desc())
                        .limit(1)
                    )
                    result = (await db.execute(sub_stmt)).scalar_one_or_none()
                    if result:
                        top_user_ids = [str(result)]

                for uid_str in top_user_ids:
                    from uuid import UUID

                    user = await db.get(User, UUID(uid_str))
                    if not user:
                        continue
                    await award_xp(db, user.id, CONTEST_WIN_XP, f"contest_win:{contest.id}")
                    await check_badges(db, user.id)
                    logger.info("Awarded contest winner %s for contest %s", user.id, contest.id)

                contest.is_active = False
                closed += 1
            except Exception as exc:
                logger.exception("Failed to close contest %s: %s", contest.id, exc)

        if closed:
            await db.commit()
    return closed


async def scheduler_loop(interval_seconds: int = 60) -> None:
    """Run periodic tasks forever. Cancelled by the FastAPI lifespan shutdown."""
    while True:
        try:
            n = await close_expired_contests()
            if n:
                logger.info("scheduler: closed %d expired contest(s)", n)
        except Exception as exc:
            logger.exception("scheduler loop error: %s", exc)
        await asyncio.sleep(interval_seconds)
