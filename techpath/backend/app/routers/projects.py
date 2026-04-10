from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.project import Project, UserProject
from app.models.user import User
from app.schemas.content import ProjectOut
from app.services.xp import award_xp

router = APIRouter()


class MilestoneUpdate(BaseModel):
    milestone_index: int
    completed: bool = True
    xp_reward: int = 30


class ProjectSubmitRequest(BaseModel):
    github_url: str
    live_url: str | None = None


@router.get("", response_model=list[ProjectOut])
async def list_projects(
    year: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[ProjectOut]:
    stmt = select(Project)
    if year:
        stmt = stmt.where(Project.year_recommended == year)
    stmt = stmt.order_by(Project.year_recommended, Project.title)
    rows = (await db.execute(stmt)).scalars().all()
    return [ProjectOut.model_validate(p) for p in rows]


@router.post("/{project_id}/start")
async def start_project(
    project_id: UUID,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")

    existing = (
        await db.execute(
            select(UserProject).where(
                UserProject.user_id == current.id,
                UserProject.project_id == project_id,
            )
        )
    ).scalar_one_or_none()
    if existing:
        return {"id": str(existing.id), "status": existing.status}

    up = UserProject(user_id=current.id, project_id=project_id)
    db.add(up)
    await db.flush()
    return {"id": str(up.id), "status": up.status}


@router.post("/{project_id}/milestone")
async def update_milestone(
    project_id: UUID,
    payload: MilestoneUpdate,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    up = (
        await db.execute(
            select(UserProject).where(
                UserProject.user_id == current.id,
                UserProject.project_id == project_id,
            )
        )
    ).scalar_one_or_none()
    if not up:
        raise HTTPException(status_code=404, detail="project not started")

    completed = list(up.milestones_completed or [])
    if payload.completed and payload.milestone_index not in completed:
        completed.append(payload.milestone_index)
        await award_xp(db, current.id, payload.xp_reward, f"project_milestone:{project_id}")
    up.milestones_completed = completed
    await db.flush()
    return {"milestones_completed": completed}


@router.post("/{project_id}/submit")
async def submit_project(
    project_id: UUID,
    payload: ProjectSubmitRequest,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    up = (
        await db.execute(
            select(UserProject).where(
                UserProject.user_id == current.id,
                UserProject.project_id == project_id,
            )
        )
    ).scalar_one_or_none()
    if not up:
        raise HTTPException(status_code=404, detail="project not started")

    up.github_url = payload.github_url
    up.live_url = payload.live_url
    up.status = "submitted"
    from datetime import datetime, timezone
    up.submitted_at = datetime.now(timezone.utc)
    await db.flush()
    return {"status": "submitted"}
