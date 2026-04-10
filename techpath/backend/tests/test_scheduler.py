from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contest import Contest, ContestSubmission
from app.models.problem import Problem
from app.models.user import User
from app.security import hash_password
from app.services.scheduler import close_expired_contests


def _make_user(email: str) -> User:
    return User(
        name=email.split("@")[0],
        email=email,
        password_hash=hash_password("pw12345678"),
        year=2,
        branch="CSE",
        goal="job",
        preferred_language="python",
    )


@pytest.mark.asyncio
async def test_close_expired_contests_marks_inactive(db_session: AsyncSession):
    now = datetime.now(timezone.utc)
    expired = Contest(
        title="Expired Contest",
        description="done",
        start_time=now - timedelta(hours=2),
        end_time=now - timedelta(minutes=30),
        problem_ids=[],
        is_active=True,
    )
    upcoming = Contest(
        title="Future Contest",
        description="later",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=2, minutes=30),
        problem_ids=[],
        is_active=True,
    )
    db_session.add_all([expired, upcoming])
    await db_session.commit()

    n = await close_expired_contests()
    assert n >= 1

    await db_session.refresh(expired)
    await db_session.refresh(upcoming)
    assert expired.is_active is False
    assert upcoming.is_active is True


@pytest.mark.asyncio
async def test_close_expired_contests_awards_winner_xp(db_session: AsyncSession):
    now = datetime.now(timezone.utc)

    winner = _make_user("winner@x.com")
    runner_up = _make_user("runner@x.com")
    db_session.add_all([winner, runner_up])

    problem = Problem(
        title="Dummy",
        slug="dummy-for-contest",
        description="x",
        difficulty=1,
        tags=["basics"],
        xp_reward=20,
    )
    db_session.add(problem)
    await db_session.flush()

    contest = Contest(
        title="Closed Contest",
        description="ended",
        start_time=now - timedelta(hours=2),
        end_time=now - timedelta(minutes=1),
        problem_ids=[problem.id],
        is_active=True,
    )
    db_session.add(contest)
    await db_session.flush()

    db_session.add_all([
        ContestSubmission(
            contest_id=contest.id,
            user_id=winner.id,
            problem_id=problem.id,
            points=500,
            time_taken_seconds=600,
        ),
        ContestSubmission(
            contest_id=contest.id,
            user_id=runner_up.id,
            problem_id=problem.id,
            points=250,
            time_taken_seconds=700,
        ),
    ])
    await db_session.commit()

    starting_xp = winner.xp_total
    await close_expired_contests()

    await db_session.refresh(winner)
    assert winner.xp_total >= starting_xp + 500
