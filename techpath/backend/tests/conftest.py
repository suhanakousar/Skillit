"""Pytest fixtures for TechPath backend tests.

DB-backed tests require a real PostgreSQL instance because several models use
Postgres-only types (JSONB, ARRAY, UUID). Set TEST_DATABASE_URL to point at an
empty test database, or start the one from docker-compose:

    docker compose -f infra/docker-compose.yml up -d postgres
    TEST_DATABASE_URL=postgresql+asyncpg://techpath:techpath@localhost:5432/techpath_test pytest

Pure unit tests (app.security, app.services.judge0 normalize) have no DB
dependency and always run.
"""
import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio

os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault(
    "DATABASE_URL",
    os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://techpath:techpath@localhost:5432/techpath_test",
    ),
)

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine():
    url = os.environ["DATABASE_URL"]
    try:
        eng = create_async_engine(url, echo=False)
        async with eng.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except Exception as exc:
        pytest.skip(f"postgres test DB not available at {url}: {exc}")
        return
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncGenerator:
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    from httpx import ASGITransport, AsyncClient

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
