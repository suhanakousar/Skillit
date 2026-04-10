import pytest

from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password_roundtrip():
    hashed = hash_password("hunter2hunter")
    assert hashed != "hunter2hunter"
    assert verify_password("hunter2hunter", hashed)
    assert not verify_password("wrong", hashed)


def test_access_token_has_correct_type():
    token = create_access_token("user-id-123")
    payload = decode_token(token)
    assert payload["sub"] == "user-id-123"
    assert payload["type"] == "access"


def test_refresh_token_type():
    token = create_refresh_token("user-id-123")
    payload = decode_token(token)
    assert payload["type"] == "refresh"


def test_invalid_token_raises():
    with pytest.raises(ValueError):
        decode_token("garbage-garbage-garbage")
