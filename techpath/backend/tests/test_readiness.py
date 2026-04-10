import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.career import JobProfile
from app.models.user import User
from app.security import hash_password
from app.services.readiness import calculate_job_readiness


@pytest.mark.asyncio
async def test_readiness_with_no_progress(db_session: AsyncSession):
    user = User(
        name="Fresh",
        email="fresh@x.com",
        password_hash=hash_password("pw12345678"),
        year=2,
        branch="CSE",
        goal="job",
        preferred_language="python",
    )
    db_session.add(user)

    job = JobProfile(
        slug="test-amazon",
        company_name="Amazon",
        role_title="SDE-1",
        package_lpa=40.0,
        difficulty_level=4,
        required_skills=[
            {"area": "dsa", "required_percent": 80},
            {"area": "projects", "required_percent": 60},
            {"area": "behavioral", "required_percent": 50},
        ],
    )
    db_session.add(job)
    await db_session.flush()

    result = await calculate_job_readiness(db_session, user.id, job.id)

    assert result["company_name"] == "Amazon"
    assert result["overall_readiness"] >= 0
    assert len(result["breakdown"]) == 3
    assert all(area["gap"] >= 0 for area in result["breakdown"])
    assert result["next_milestone"]


@pytest.mark.asyncio
async def test_readiness_missing_job_raises(db_session: AsyncSession):
    from uuid import uuid4

    user = User(
        name="U",
        email="u@x.com",
        password_hash=hash_password("pw12345678"),
        year=2,
        branch="CSE",
        goal="job",
        preferred_language="python",
    )
    db_session.add(user)
    await db_session.flush()

    with pytest.raises(ValueError, match="job profile not found"):
        await calculate_job_readiness(db_session, user.id, uuid4())
