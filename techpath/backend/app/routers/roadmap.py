from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.lesson import UserProgress
from app.models.roadmap import RoadmapNode
from app.models.track import Track
from app.models.user import User
from app.schemas.content import TrackOut

router = APIRouter()


@router.get("")
async def get_roadmap(
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    nodes = (
        (await db.execute(select(RoadmapNode).order_by(RoadmapNode.year, RoadmapNode.position_x)))
        .scalars()
        .all()
    )

    completed_track_ids = set(
        (
            await db.execute(
                select(UserProgress.track_id)
                .where(UserProgress.user_id == current.id, UserProgress.status == "completed")
                .distinct()
            )
        ).scalars()
    )

    in_progress_track_ids = set(
        (
            await db.execute(
                select(UserProgress.track_id)
                .where(UserProgress.user_id == current.id, UserProgress.status == "in_progress")
                .distinct()
            )
        ).scalars()
    )

    out_nodes = []
    for n in nodes:
        if n.track_id in completed_track_ids:
            state = "completed"
        elif n.track_id in in_progress_track_ids:
            state = "active"
        elif all(pid in completed_track_ids for pid in (n.prerequisite_node_ids or [])):
            state = "unlocked"
        else:
            state = "locked"
        out_nodes.append({
            "id": str(n.id),
            "year": n.year,
            "domain": n.domain,
            "title": n.title,
            "description": n.description,
            "track_id": str(n.track_id) if n.track_id else None,
            "prerequisite_node_ids": [str(p) for p in (n.prerequisite_node_ids or [])],
            "position_x": n.position_x,
            "position_y": n.position_y,
            "state": state,
        })

    return {"nodes": out_nodes}


@router.get("/tracks", response_model=list[TrackOut])
async def list_tracks(db: AsyncSession = Depends(get_db)) -> list[TrackOut]:
    stmt = select(Track).order_by(Track.year_recommended, Track.order_index)
    tracks = (await db.execute(stmt)).scalars().all()
    return [TrackOut.model_validate(t) for t in tracks]
