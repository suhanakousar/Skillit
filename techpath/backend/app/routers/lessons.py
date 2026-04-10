from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.lesson import Lesson, UserProgress
from app.models.user import User
from app.schemas.content import LessonOut, LessonSummary
from app.services.badges import check_badges
from app.services.streak import register_activity
from app.services.xp import award_xp

router = APIRouter()


@router.get("/track/{track_id}", response_model=list[LessonSummary])
async def list_lessons(
    track_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> list[LessonSummary]:
    stmt = select(Lesson).where(Lesson.track_id == track_id).order_by(Lesson.order_index)
    lessons = (await db.execute(stmt)).scalars().all()
    return [LessonSummary.model_validate(l) for l in lessons]


@router.get("/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: UUID, db: AsyncSession = Depends(get_db)) -> LessonOut:
    lesson = await db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="lesson not found")
    return LessonOut.model_validate(lesson)


@router.post("/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: UUID,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    lesson = await db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="lesson not found")

    existing = (
        await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == current.id,
                UserProgress.lesson_id == lesson_id,
            )
        )
    ).scalar_one_or_none()

    already_done = existing and existing.status == "completed"

    if not existing:
        db.add(
            UserProgress(
                user_id=current.id,
                track_id=lesson.track_id,
                lesson_id=lesson_id,
                status="completed",
                score=100,
            )
        )
    else:
        existing.status = "completed"
        existing.score = 100

    xp_awarded = 0
    if not already_done:
        xp_awarded = lesson.xp_reward
        await award_xp(db, current.id, xp_awarded, f"lesson:{lesson.id}")

    streak = await register_activity(db, current.id)
    new_badges = await check_badges(db, current.id)

    return {
        "xp_awarded": xp_awarded,
        "streak": streak,
        "new_badges": [{"slug": b.slug, "name": b.name} for b in new_badges],
    }
