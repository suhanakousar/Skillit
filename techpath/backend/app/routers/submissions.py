from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.problem import Problem, Submission
from app.models.user import User
from app.schemas.content import SubmissionCreate, SubmissionResult, TestCaseResult
from app.services.badges import check_badges
from app.services.judge0 import judge0
from app.services.streak import register_activity
from app.services.xp import award_xp

router = APIRouter()


@router.post("", response_model=SubmissionResult)
async def submit(
    payload: SubmissionCreate,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SubmissionResult:
    problem = await db.get(Problem, payload.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")

    test_cases = problem.test_cases_json or []
    test_results: list[TestCaseResult] = []
    aggregate_status = "accepted"
    max_runtime = 0
    max_memory = 0

    for idx, tc in enumerate(test_cases):
        stdin = tc.get("input", "")
        expected = tc.get("output", "")
        result = await judge0.submit(payload.language, payload.code, stdin, expected)

        test_results.append(
            TestCaseResult(
                index=idx,
                status=result["status"],
                stdout=result.get("stdout"),
                expected=expected,
                runtime_ms=result.get("runtime_ms"),
            )
        )

        max_runtime = max(max_runtime, result.get("runtime_ms") or 0)
        max_memory = max(max_memory, result.get("memory_kb") or 0)

        if result["status"] != "accepted":
            aggregate_status = result["status"]
            break

    prior_accepted = (
        await db.execute(
            select(func.count(Submission.id)).where(
                Submission.user_id == current.id,
                Submission.problem_id == problem.id,
                Submission.status == "accepted",
            )
        )
    ).scalar_one()

    xp_awarded = 0
    if aggregate_status == "accepted" and prior_accepted == 0:
        xp_awarded = problem.xp_reward

    submission = Submission(
        user_id=current.id,
        problem_id=problem.id,
        language=payload.language,
        code=payload.code,
        status=aggregate_status,
        runtime_ms=max_runtime,
        memory_kb=max_memory,
        percentile=None,
        test_results_json=[tr.model_dump() for tr in test_results],
    )
    db.add(submission)
    await db.flush()

    if xp_awarded:
        await award_xp(db, current.id, xp_awarded, f"problem:{problem.slug}")

    if aggregate_status == "accepted":
        await register_activity(db, current.id)
        await check_badges(db, current.id)

    return SubmissionResult(
        id=submission.id,
        status=aggregate_status,
        runtime_ms=max_runtime,
        memory_kb=max_memory,
        percentile=None,
        xp_awarded=xp_awarded,
        test_results=test_results,
        submitted_at=submission.submitted_at,
    )


@router.get("/me/problem/{problem_id}")
async def history_for_problem(
    problem_id: UUID,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    stmt = (
        select(Submission)
        .where(Submission.user_id == current.id, Submission.problem_id == problem_id)
        .order_by(Submission.submitted_at.desc())
        .limit(50)
    )
    subs = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(s.id),
            "language": s.language,
            "status": s.status,
            "runtime_ms": s.runtime_ms,
            "submitted_at": s.submitted_at.isoformat(),
        }
        for s in subs
    ]
