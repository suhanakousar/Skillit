from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TrackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    domain: str
    description: str | None
    year_recommended: int
    order_index: int
    prerequisite_track_ids: list[UUID]
    total_xp: int
    estimated_hours: int
    icon: str | None


class LessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    type: str
    xp_reward: int
    order_index: int
    duration_minutes: int


class LessonOut(LessonSummary):
    track_id: UUID
    content_json: dict[str, Any]


class ProblemSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    difficulty: int
    tags: list[str]
    xp_reward: int


class ProblemDetail(ProblemSummary):
    description: str
    starter_code_json: dict[str, Any]
    examples_json: list[Any]
    constraints_text: str | None
    hints_json: list[Any]


class SubmissionCreate(BaseModel):
    problem_id: UUID
    language: str
    code: str


class TestCaseResult(BaseModel):
    index: int
    status: str
    stdout: str | None = None
    expected: str | None = None
    runtime_ms: int | None = None


class SubmissionResult(BaseModel):
    id: UUID
    status: str
    runtime_ms: int | None
    memory_kb: int | None
    percentile: float | None
    xp_awarded: int
    test_results: list[TestCaseResult]
    submitted_at: datetime


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    description: str
    tech_stack: list[str]
    milestones_json: list[Any]
    year_recommended: int | None
    xp_total: int
    repo_template_url: str | None


class BadgeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    description: str
    icon: str | None
    xp_bonus: int


class ContestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    problem_ids: list[UUID]
    is_active: bool


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: UUID
    name: str
    college: str | None
    xp_total: int
    streak_current: int


class ReadinessArea(BaseModel):
    area: str
    required: int
    current: int
    gap: int
    action: str


class ReadinessResult(BaseModel):
    job_profile_id: UUID
    company_name: str
    role_title: str
    overall_readiness: int
    breakdown: list[ReadinessArea]
    estimated_weeks_to_ready: int
    next_milestone: str
