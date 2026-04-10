from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.problem import Problem, Submission
from app.models.user import User
from app.schemas.content import (
    RunCreate,
    RunResult,
    SubmissionCreate,
    SubmissionResult,
    TestCaseResult,
)
from app.services.badges import check_badges
from app.services.judge0 import judge0
from app.services.streak import register_activity
from app.services.xp import award_xp

router = APIRouter()


def _is_compile_error(stderr: str | None) -> bool:
    """Cheap heuristic for Python syntax errors reported by the local runner."""
    if not stderr:
        return False
    lowered = stderr.lower()
    return (
        "syntaxerror" in lowered
        or "indentationerror" in lowered
        or "compile error" in lowered
    )


@router.post("/run", response_model=RunResult)
async def run(
    payload: RunCreate,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RunResult:
    """Fast, non-persisting run — LeetCode-style 'Run' button.

    Runs the user's code against the visible `examples_json` cases (or a single
    custom stdin the user provides) and returns stdout/stderr/verdict for each.
    Nothing is saved to the DB; no XP is awarded. Safe to call repeatedly.
    """
    problem = await db.get(Problem, payload.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")

    if payload.custom_stdin is not None:
        cases = [{"input": payload.custom_stdin, "output": None}]
    else:
        cases = list(problem.examples_json or [])
        if not cases:
            # Fall back to the first hidden test so the user sees something
            # useful instead of an empty console.
            first = (problem.test_cases_json or [{}])[0]
            cases = [{"input": first.get("input", ""), "output": first.get("output", "")}]

    compile_error: str | None = None
    results: list[TestCaseResult] = []
    overall = "accepted"

    for idx, case in enumerate(cases):
        stdin = case.get("input", "") or ""
        expected = case.get("output")
        raw = await judge0.submit(payload.language, payload.code, stdin, expected or "")

        status = raw["status"]
        stderr = raw.get("stderr") or None

        # For custom stdin we have no expected output — never call it wrong.
        if expected is None and status == "wrong_answer":
            status = "accepted"

        if status == "compile_error" and not compile_error:
            compile_error = stderr or "compile error"

        results.append(
            TestCaseResult(
                index=idx,
                status=status,
                stdin=stdin,
                stdout=raw.get("stdout"),
                expected=expected,
                stderr=stderr,
                runtime_ms=raw.get("runtime_ms"),
            )
        )

        if status != "accepted" and overall == "accepted":
            overall = status

    return RunResult(status=overall, compile_error=compile_error, results=results)


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
    total = len(test_cases)
    passed = 0
    test_results: list[TestCaseResult] = []
    failing_test: TestCaseResult | None = None
    aggregate_status = "accepted"
    compile_error: str | None = None
    max_runtime = 0
    max_memory = 0

    for idx, tc in enumerate(test_cases):
        stdin = tc.get("input", "")
        expected = tc.get("output", "")
        result = await judge0.submit(payload.language, payload.code, stdin, expected)
        stderr = result.get("stderr") or None

        tr = TestCaseResult(
            index=idx,
            status=result["status"],
            stdin=stdin,
            stdout=result.get("stdout"),
            expected=expected,
            stderr=stderr,
            runtime_ms=result.get("runtime_ms"),
        )
        test_results.append(tr)

        max_runtime = max(max_runtime, result.get("runtime_ms") or 0)
        max_memory = max(max_memory, result.get("memory_kb") or 0)

        if result["status"] == "accepted":
            passed += 1
            continue

        # First failure: capture details and stop (LeetCode-style early exit).
        aggregate_status = result["status"]
        failing_test = tr
        if result["status"] == "compile_error" or _is_compile_error(stderr):
            aggregate_status = "compile_error"
            compile_error = stderr or "compile error"
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
        passed=passed,
        total=total,
        compile_error=compile_error,
        failing_test=failing_test,
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
