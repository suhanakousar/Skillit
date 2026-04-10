from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, get_db
from app.deps import get_current_user
from app.models.contest import Contest, ContestSubmission
from app.models.user import User
from app.redis_client import redis
from app.schemas.content import ContestOut

router = APIRouter()


POINTS_BY_DIFFICULTY = {1: 100, 2: 100, 3: 250, 4: 500, 5: 500}
PENALTY = 5


class ContestSubmitRequest(BaseModel):
    problem_id: UUID
    submission_id: UUID
    status: str
    difficulty: int = 1


@router.get("", response_model=list[ContestOut])
async def list_contests(db: AsyncSession = Depends(get_db)) -> list[ContestOut]:
    stmt = select(Contest).order_by(Contest.start_time.desc())
    rows = (await db.execute(stmt)).scalars().all()
    return [ContestOut.model_validate(c) for c in rows]


@router.get("/active", response_model=ContestOut | None)
async def active_contest(db: AsyncSession = Depends(get_db)) -> ContestOut | None:
    now = datetime.now(timezone.utc)
    stmt = (
        select(Contest)
        .where(Contest.is_active.is_(True), Contest.start_time <= now, Contest.end_time >= now)
        .limit(1)
    )
    row = (await db.execute(stmt)).scalar_one_or_none()
    return ContestOut.model_validate(row) if row else None


@router.post("/{contest_id}/submit")
async def submit_to_contest(
    contest_id: UUID,
    payload: ContestSubmitRequest,
    current: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    contest = await db.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="contest not found")

    now = datetime.now(timezone.utc)
    if not (contest.start_time <= now <= contest.end_time):
        raise HTTPException(status_code=400, detail="contest not live")

    base_points = POINTS_BY_DIFFICULTY.get(payload.difficulty, 100)
    points = base_points if payload.status == "accepted" else -PENALTY

    cs = ContestSubmission(
        contest_id=contest.id,
        user_id=current.id,
        problem_id=payload.problem_id,
        submission_id=payload.submission_id,
        points=points,
        time_taken_seconds=int((now - contest.start_time).total_seconds()),
    )
    db.add(cs)
    await db.flush()

    try:
        await redis.zincrby(f"contest:{contest_id}:leaderboard", points, str(current.id))
    except Exception:
        pass

    return {"points_awarded": points}


@router.get("/{contest_id}/leaderboard")
async def contest_leaderboard(
    contest_id: UUID,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    try:
        entries = await redis.zrevrange(
            f"contest:{contest_id}:leaderboard", 0, limit - 1, withscores=True
        )
    except Exception:
        entries = []

    if not entries:
        return []

    from uuid import UUID as UUID_

    ids = [UUID_(uid) for uid, _ in entries]
    result = await db.execute(select(User).where(User.id.in_(ids)))
    users_by_id = {str(u.id): u for u in result.scalars()}

    out = []
    for rank, (uid, score) in enumerate(entries, start=1):
        u = users_by_id.get(uid)
        if not u:
            continue
        out.append(
            {
                "rank": rank,
                "user_id": uid,
                "name": u.name,
                "college": u.college,
                "points": int(score),
            }
        )
    return out


@router.websocket("/{contest_id}/live")
async def contest_live(websocket: WebSocket, contest_id: UUID):
    """Push leaderboard updates every 5 seconds to connected clients."""
    import asyncio

    await websocket.accept()
    try:
        while True:
            async with AsyncSessionLocal() as db:
                board = await contest_leaderboard(contest_id, 20, db)
            await websocket.send_json({"leaderboard": board})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        return
