from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.redis_client import redis

XP_REWARDS = {
    "story_lesson": 10,
    "interactive_lesson": 15,
    "codealong_lesson": 20,
    "easy_problem": 20,
    "medium_problem": 50,
    "hard_problem": 150,
    "project_milestone_min": 30,
    "project_milestone_max": 100,
    "track_complete": 300,
    "contest_win": 500,
    "streak_7": 100,
    "streak_30": 500,
}


async def award_xp(db: AsyncSession, user_id: UUID, amount: int, reason: str) -> int:
    """Atomically add XP to a user and update the global Redis leaderboard.

    Returns the user's new total XP.
    """
    user = await db.get(User, user_id)
    if not user:
        return 0
    user.xp_total += amount
    await db.flush()

    try:
        await redis.zadd("leaderboard:global", {str(user.id): user.xp_total})
        if user.college:
            await redis.zadd(f"leaderboard:college:{user.college}", {str(user.id): user.xp_total})
    except Exception:
        pass

    return user.xp_total


async def get_leaderboard(college: str | None = None, limit: int = 50) -> list[dict]:
    """Fetch leaderboard entries from Redis with a DB fallback."""
    key = f"leaderboard:college:{college}" if college else "leaderboard:global"
    try:
        entries = await redis.zrevrange(key, 0, limit - 1, withscores=True)
        if entries:
            return [
                {"rank": i + 1, "user_id": uid, "xp_total": int(score)}
                for i, (uid, score) in enumerate(entries)
            ]
    except Exception:
        pass
    return []


async def get_leaderboard_with_users(
    db: AsyncSession,
    college: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """Leaderboard enriched with name/college/streak from the DB.

    Falls back to a direct DB query if Redis is empty or unavailable.
    """
    redis_entries = await get_leaderboard(college, limit)

    if redis_entries:
        ids = [UUID(e["user_id"]) for e in redis_entries]
        result = await db.execute(select(User).where(User.id.in_(ids)))
        users_by_id = {str(u.id): u for u in result.scalars()}
        out = []
        for entry in redis_entries:
            u = users_by_id.get(entry["user_id"])
            if not u:
                continue
            out.append({
                "rank": entry["rank"],
                "user_id": u.id,
                "name": u.name,
                "college": u.college,
                "xp_total": u.xp_total,
                "streak_current": u.streak_current,
            })
        return out

    stmt = select(User).order_by(User.xp_total.desc()).limit(limit)
    if college:
        stmt = select(User).where(User.college == college).order_by(User.xp_total.desc()).limit(limit)
    result = await db.execute(stmt)
    users = list(result.scalars())
    return [
        {
            "rank": i + 1,
            "user_id": u.id,
            "name": u.name,
            "college": u.college,
            "xp_total": u.xp_total,
            "streak_current": u.streak_current,
        }
        for i, u in enumerate(users)
    ]
