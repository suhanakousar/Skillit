from datetime import date, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.xp import XP_REWARDS, award_xp


async def register_activity(db: AsyncSession, user_id: UUID) -> dict:
    """Record a daily activity ping and update streak counters.

    Returns the streak state and any bonus XP awarded for streak milestones.
    """
    user = await db.get(User, user_id)
    if not user:
        return {"streak_current": 0, "streak_max": 0, "bonus_xp": 0}

    today = date.today()
    last = user.last_active_date
    bonus = 0

    if last == today:
        return {
            "streak_current": user.streak_current,
            "streak_max": user.streak_max,
            "bonus_xp": 0,
        }
    if last == today - timedelta(days=1):
        user.streak_current += 1
    else:
        user.streak_current = 1

    user.last_active_date = today
    if user.streak_current > user.streak_max:
        user.streak_max = user.streak_current

    if user.streak_current == 7:
        bonus = XP_REWARDS["streak_7"]
    elif user.streak_current == 30:
        bonus = XP_REWARDS["streak_30"]

    await db.flush()

    if bonus:
        await award_xp(db, user_id, bonus, f"streak_{user.streak_current}")

    return {
        "streak_current": user.streak_current,
        "streak_max": user.streak_max,
        "bonus_xp": bonus,
    }
