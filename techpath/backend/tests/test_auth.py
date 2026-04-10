import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup_and_login_flow(client: AsyncClient):
    payload = {
        "name": "Test Student",
        "email": "test@klu.ac.in",
        "password": "hunter2hunter",
        "year": 2,
        "branch": "CSE",
        "goal": "job",
        "preferred_language": "python",
        "college": "KL University",
    }
    r = await client.post("/api/auth/signup", json=payload)
    assert r.status_code == 201, r.text
    tokens = r.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    dup = await client.post("/api/auth/signup", json=payload)
    assert dup.status_code == 409

    login = await client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    bad = await client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": "wrong-password"},
    )
    assert bad.status_code == 401

    access = tokens["access_token"]
    me = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {access}"})
    assert me.status_code == 200
    body = me.json()
    assert body["email"] == payload["email"]
    assert body["branch"] == "CSE"
    assert body["year"] == 2
