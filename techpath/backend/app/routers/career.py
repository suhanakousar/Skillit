from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.career import JobProfile
from app.models.user import User
from app.schemas.content import ReadinessResult
from app.services.readiness import calculate_job_readiness

router = APIRouter()


@router.get("/jobs")
async def list_jobs(db: AsyncSession = Depends(get_db)) -> list[dict]:
    stmt = select(JobProfile).order_by(JobProfile.difficulty_level)
    rows = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(j.id),
            "slug": j.slug,
            "company_name": j.company_name,
            "role_title": j.role_title,
            "package_lpa": float(j.package_lpa) if j.package_lpa else None,
            "difficulty_level": j.difficulty_level,
        }
        for j in rows
    ]


@router.get("/readiness/{job_profile_id}", response_model=ReadinessResult)
async def readiness(
    job_profile_id: UUID,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReadinessResult:
    result = await calculate_job_readiness(db, current.id, job_profile_id)
    return ReadinessResult(**result)


@router.get("/readiness")
async def readiness_all(
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    jobs = (await db.execute(select(JobProfile))).scalars().all()
    out = []
    for j in jobs:
        r = await calculate_job_readiness(db, current.id, j.id)
        out.append(
            {
                "job_profile_id": str(j.id),
                "company_name": j.company_name,
                "role_title": j.role_title,
                "overall_readiness": r["overall_readiness"],
                "next_milestone": r["next_milestone"],
            }
        )
    return out
