from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.problem import Problem
from app.schemas.content import ProblemDetail, ProblemSummary

router = APIRouter()


@router.get("", response_model=list[ProblemSummary])
async def list_problems(
    difficulty: int | None = Query(None, ge=1, le=5),
    tag: str | None = None,
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[ProblemSummary]:
    stmt = select(Problem)
    if difficulty:
        stmt = stmt.where(Problem.difficulty == difficulty)
    if tag:
        stmt = stmt.where(Problem.tags.any(tag))
    stmt = stmt.order_by(Problem.difficulty, Problem.title).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return [ProblemSummary.model_validate(p) for p in rows]


@router.get("/{problem_id}", response_model=ProblemDetail)
async def get_problem(problem_id: UUID, db: AsyncSession = Depends(get_db)) -> ProblemDetail:
    problem = await db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    return ProblemDetail.model_validate(problem)


@router.get("/by-slug/{slug}", response_model=ProblemDetail)
async def get_problem_by_slug(slug: str, db: AsyncSession = Depends(get_db)) -> ProblemDetail:
    result = await db.execute(select(Problem).where(Problem.slug == slug))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    return ProblemDetail.model_validate(problem)
