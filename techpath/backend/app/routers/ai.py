from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.problem import Problem
from app.models.user import User
from app.schemas.ai import ExplainRequest, HintRequest, ReviewRequest, StoryLessonRequest
from app.services.claude_ai import (
    generate_hint,
    review_code,
    stream_explanation,
    stream_story_lesson,
)

router = APIRouter()


@router.post("/explain")
async def explain(
    payload: ExplainRequest,
    _: User = Depends(get_current_user),
) -> StreamingResponse:
    return StreamingResponse(
        stream_explanation(payload.concept, payload.user_year, payload.user_language),
        media_type="text/plain",
    )


@router.post("/hint")
async def hint(
    payload: HintRequest,
    _: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    problem = await db.get(Problem, payload.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")

    text = await generate_hint(
        problem.title, problem.description, payload.hint_level, payload.user_code
    )
    return {"level": payload.hint_level, "text": text}


@router.post("/review")
async def review(
    payload: ReviewRequest,
    _: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    problem_title: str | None = None
    if payload.problem_id:
        problem = await db.get(Problem, payload.problem_id)
        if problem:
            problem_title = problem.title

    return await review_code(payload.code, payload.language, problem_title)


@router.post("/story-lesson")
async def story_lesson(
    payload: StoryLessonRequest,
    _: User = Depends(get_current_user),
) -> StreamingResponse:
    return StreamingResponse(
        stream_story_lesson(payload.topic, payload.user_year, payload.user_language, payload.user_goal),
        media_type="text/plain",
    )
