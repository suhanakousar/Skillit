from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, SignupRequest, TokenPair
from app.schemas.user import UserPublic
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter()


@router.post("/signup", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        year=payload.year,
        branch=payload.branch,
        goal=payload.goal,
        preferred_language=payload.preferred_language,
        college=payload.college,
    )
    db.add(user)
    await db.flush()

    return TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")

    return TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest) -> TokenPair:
    try:
        data = decode_token(payload.refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="invalid refresh token")
    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="wrong token type")

    sub = data["sub"]
    return TokenPair(
        access_token=create_access_token(sub),
        refresh_token=create_refresh_token(sub),
    )


@router.post("/demo-login", response_model=TokenPair)
async def demo_login(db: AsyncSession = Depends(get_db)) -> TokenPair:
    """Issue tokens for the seeded demo account if it exists.

    Returns 404 if the demo user hasn't been seeded (e.g. SEED_DEMO_USER=false).
    """
    if not settings.seed_demo_user:
        raise HTTPException(status_code=404, detail="demo account disabled")

    result = await db.execute(select(User).where(User.email == settings.demo_email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="demo account not seeded yet")

    return TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)
