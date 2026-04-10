from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    year: int
    branch: str
    goal: str
    preferred_language: str
    college: str | None
    xp_total: int
    streak_current: int
    streak_max: int
    last_active_date: date | None
    created_at: datetime


class DashboardPayload(BaseModel):
    user: UserPublic
    tracks_in_progress: int
    lessons_completed: int
    problems_solved: int
    badges_earned: int
    next_recommended_action: str
