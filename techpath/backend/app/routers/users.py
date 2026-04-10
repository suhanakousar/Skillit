from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.badge import UserBadge
from app.models.lesson import UserProgress
from app.models.problem import Submission
from app.models.user import User
from app.schemas.content import BadgeOut, LeaderboardEntry
from app.schemas.user import DashboardPayload, UserPublic
from app.services.xp import get_leaderboard_with_users

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def get_me(current: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current)


@router.get("/dashboard", response_model=DashboardPayload)
async def dashboard(
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardPayload:
    lessons_completed = (
        await db.execute(
            select(func.count(UserProgress.id)).where(
                UserProgress.user_id == current.id,
                UserProgress.status == "completed",
            )
        )
    ).scalar_one()

    tracks_in_progress = (
        await db.execute(
            select(func.count(func.distinct(UserProgress.track_id))).where(
                UserProgress.user_id == current.id,
                UserProgress.status == "in_progress",
            )
        )
    ).scalar_one()

    problems_solved = (
        await db.execute(
            select(func.count(func.distinct(Submission.problem_id))).where(
                Submission.user_id == current.id,
                Submission.status == "accepted",
            )
        )
    ).scalar_one()

    badges_earned = (
        await db.execute(
            select(func.count(UserBadge.id)).where(UserBadge.user_id == current.id)
        )
    ).scalar_one()

    next_action = _recommend_next_action(
        lessons_completed, problems_solved, current.streak_current
    )

    return DashboardPayload(
        user=UserPublic.model_validate(current),
        tracks_in_progress=tracks_in_progress,
        lessons_completed=lessons_completed,
        problems_solved=problems_solved,
        badges_earned=badges_earned,
        next_recommended_action=next_action,
    )


def _recommend_next_action(lessons: int, problems: int, streak: int) -> str:
    if lessons == 0:
        return "Start your first story lesson"
    if problems == 0:
        return "Solve your first easy problem to earn +20 XP"
    if streak < 3:
        return "Come back tomorrow to extend your streak"
    if problems < 10:
        return "Push for 10 problems — unlock 'Array Master' badge"
    return "Try a medium-difficulty problem next"


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def leaderboard(
    scope: str = "global",
    limit: int = 50,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[LeaderboardEntry]:
    college = current.college if scope == "college" else None
    entries = await get_leaderboard_with_users(db, college=college, limit=limit)
    return [LeaderboardEntry(**e) for e in entries]


@router.get("/me/badges", response_model=list[BadgeOut])
async def my_badges(
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[BadgeOut]:
    from app.models.badge import Badge

    stmt = (
        select(Badge)
        .join(UserBadge, UserBadge.badge_id == Badge.id)
        .where(UserBadge.user_id == current.id)
    )
    badges = (await db.execute(stmt)).scalars().all()
    return [BadgeOut.model_validate(b) for b in badges]
