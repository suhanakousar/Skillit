from typing import Literal

from pydantic import BaseModel, EmailStr, Field


Branch = Literal["CSE", "AIDS", "AIML", "IoT", "ECE", "OTHER"]
Goal = Literal["job", "gate", "startup", "research"]
Language = Literal["python", "cpp", "java", "javascript", "c", "go"]


class SignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    year: int = Field(ge=1, le=4)
    branch: Branch
    goal: Goal
    preferred_language: Language = "python"
    college: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
