from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.badge import Badge, UserBadge
from app.models.problem import Problem, Submission
from app.models.user import User
from app.services.xp import award_xp


async def _count_accepted(db: AsyncSession, user_id: UUID) -> int:
    stmt = select(func.count(func.distinct(Submission.problem_id))).where(
        Submission.user_id == user_id,
        Submission.status == "accepted",
    )
    return (await db.execute(stmt)).scalar_one()


async def _count_by_tag(db: AsyncSession, user_id: UUID, tag: str) -> int:
    stmt = (
        select(func.count(func.distinct(Problem.id)))
        .join(Submission, Submission.problem_id == Problem.id)
        .where(
            Submission.user_id == user_id,
            Submission.status == "accepted",
            Problem.tags.any(tag),
        )
    )
    return (await db.execute(stmt)).scalar_one()


async def _count_by_difficulty(db: AsyncSession, user_id: UUID, difficulty: int) -> int:
    stmt = (
        select(func.count(func.distinct(Problem.id)))
        .join(Submission, Submission.problem_id == Problem.id)
        .where(
            Submission.user_id == user_id,
            Submission.status == "accepted",
            Problem.difficulty == difficulty,
        )
    )
    return (await db.execute(stmt)).scalar_one()


async def _already_earned(db: AsyncSession, user_id: UUID, badge_id: UUID) -> bool:
    stmt = select(UserBadge).where(UserBadge.user_id == user_id, UserBadge.badge_id == badge_id)
    return (await db.execute(stmt)).scalar_one_or_none() is not None


async def check_badges(db: AsyncSession, user_id: UUID) -> list[Badge]:
    """Evaluate all badge conditions for a user and award any newly unlocked badges.

    Returns the list of newly earned badges.
    """
    user = await db.get(User, user_id)
    if not user:
        return []

    badges = (await db.execute(select(Badge))).scalars().all()
    newly_earned: list[Badge] = []

    for badge in badges:
        if await _already_earned(db, user_id, badge.id):
            continue

        cond = badge.condition_json or {}
        ctype = cond.get("type")
        target = cond.get("target", 0)
        unlocked = False

        if ctype == "first_submission":
            accepted = await _count_accepted(db, user_id)
            unlocked = accepted >= 1
        elif ctype == "first_lesson":
            unlocked = user.xp_total > 0
        elif ctype == "streak":
            unlocked = user.streak_current >= target
        elif ctype == "problems_solved":
            unlocked = (await _count_accepted(db, user_id)) >= target
        elif ctype == "tag_solved":
            unlocked = (await _count_by_tag(db, user_id, cond.get("tag", ""))) >= target
        elif ctype == "difficulty_solved":
            unlocked = (await _count_by_difficulty(db, user_id, cond.get("difficulty", 5))) >= target
        elif ctype == "xp_total":
            unlocked = user.xp_total >= target

        if unlocked:
            db.add(UserBadge(user_id=user_id, badge_id=badge.id))
            newly_earned.append(badge)
            if badge.xp_bonus:
                await award_xp(db, user_id, badge.xp_bonus, f"badge:{badge.slug}")

    if newly_earned:
        await db.flush()
    return newly_earned
