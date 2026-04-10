from datetime import date, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.security import hash_password
from app.services.streak import register_activity
from app.services.xp import award_xp


async def _make_user(db: AsyncSession, **kw) -> User:
    user = User(
        name="Tester",
        email=f"{kw.get('email_prefix', 'u1')}@x.com",
        password_hash=hash_password("password1234"),
        year=2,
        branch="CSE",
        goal="job",
        preferred_language="python",
        **{k: v for k, v in kw.items() if k != "email_prefix"},
    )
    db.add(user)
    await db.flush()
    return user


@pytest.mark.asyncio
async def test_award_xp_updates_total(db_session: AsyncSession):
    user = await _make_user(db_session, email_prefix="xp-user")
    new_total = await award_xp(db_session, user.id, 50, "test")
    assert new_total == 50

    new_total = await award_xp(db_session, user.id, 30, "test2")
    assert new_total == 80

    await db_session.refresh(user)
    assert user.xp_total == 80


@pytest.mark.asyncio
async def test_streak_starts_at_one(db_session: AsyncSession):
    user = await _make_user(db_session, email_prefix="streak-user")
    result = await register_activity(db_session, user.id)
    assert result["streak_current"] == 1
    assert result["streak_max"] == 1
    assert result["bonus_xp"] == 0


@pytest.mark.asyncio
async def test_streak_same_day_is_noop(db_session: AsyncSession):
    user = await _make_user(db_session, email_prefix="streak-same")
    await register_activity(db_session, user.id)
    result = await register_activity(db_session, user.id)
    assert result["streak_current"] == 1


@pytest.mark.asyncio
async def test_streak_seven_day_bonus(db_session: AsyncSession):
    user = await _make_user(db_session, email_prefix="streak-7")
    user.streak_current = 6
    user.last_active_date = date.today() - timedelta(days=1)
    await db_session.flush()

    result = await register_activity(db_session, user.id)
    assert result["streak_current"] == 7
    assert result["bonus_xp"] == 100


@pytest.mark.asyncio
async def test_streak_resets_after_gap(db_session: AsyncSession):
    user = await _make_user(db_session, email_prefix="streak-reset")
    user.streak_current = 10
    user.streak_max = 10
    user.last_active_date = date.today() - timedelta(days=3)
    await db_session.flush()

    result = await register_activity(db_session, user.id)
    assert result["streak_current"] == 1
    assert result["streak_max"] == 10
