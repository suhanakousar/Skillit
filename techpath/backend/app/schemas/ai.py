from uuid import UUID

from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    concept: str
    user_year: int = Field(ge=1, le=4)
    user_language: str = "python"


class HintRequest(BaseModel):
    problem_id: UUID
    hint_level: int = Field(ge=1, le=3)
    user_code: str | None = None


class ReviewRequest(BaseModel):
    code: str
    language: str
    problem_id: UUID | None = None


class StoryLessonRequest(BaseModel):
    topic: str
    user_year: int = Field(ge=1, le=4)
    user_language: str = "python"
    user_goal: str = "job"
