import base64

from app.services.judge0 import Judge0Client


def _b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def test_normalize_accepted():
    data = {
        "status": {"id": 3},
        "stdout": _b64("hello\n"),
        "stderr": None,
        "time": "0.042",
        "memory": 2048,
    }
    out = Judge0Client._normalize(data)
    assert out["status"] == "accepted"
    assert out["stdout"].strip() == "hello"
    assert out["runtime_ms"] == 42
    assert out["memory_kb"] == 2048


def test_normalize_wrong_answer():
    data = {"status": {"id": 4}, "stdout": _b64("42"), "time": "0.1", "memory": 1000}
    out = Judge0Client._normalize(data)
    assert out["status"] == "wrong_answer"


def test_normalize_tle():
    data = {"status": {"id": 5}, "time": "5.0", "memory": 1000}
    out = Judge0Client._normalize(data)
    assert out["status"] == "tle"


def test_normalize_compile_error_includes_stderr():
    data = {
        "status": {"id": 6},
        "compile_output": _b64("syntax error"),
        "time": "0",
        "memory": 0,
    }
    out = Judge0Client._normalize(data)
    assert out["status"] == "compile_error"
    assert "syntax error" in out["stderr"]
