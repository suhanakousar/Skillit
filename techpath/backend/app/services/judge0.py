import asyncio
import base64
import logging
from typing import Any

import httpx

from app.config import settings
from app.services import local_runner

logger = logging.getLogger(__name__)

LANGUAGE_IDS = {
    "python": 71,
    "cpp": 54,
    "java": 62,
    "javascript": 63,
    "c": 50,
    "go": 60,
}

STATUS_NORMALIZATION = {
    3: "accepted",
    4: "wrong_answer",
    5: "tle",
    6: "compile_error",
    7: "runtime_error",
    8: "runtime_error",
    9: "runtime_error",
    10: "runtime_error",
    11: "runtime_error",
    12: "runtime_error",
    13: "runtime_error",
    14: "runtime_error",
}


def _b64(value: str | None) -> str | None:
    if value is None:
        return None
    return base64.b64encode(value.encode()).decode()


def _b64_decode(value: str | None) -> str:
    if not value:
        return ""
    try:
        return base64.b64decode(value).decode(errors="replace")
    except Exception:
        return ""


class Judge0Client:
    """Async Judge0 client with retry + local runner fallback.

    When Judge0 is unreachable and `use_local_runner_fallback` is set,
    submissions are executed in-process via `local_runner`. This lets the app
    work out of the box without having to stand up the Judge0 sandbox.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (base_url or settings.judge0_url).rstrip("/")
        self.api_key = api_key or settings.judge0_api_key
        self.timeout = httpx.Timeout(5.0, read=15.0)
        self._judge0_unavailable = False

    def _headers(self) -> dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["X-RapidAPI-Key"] = self.api_key
        return h

    async def submit(
        self,
        language: str,
        source_code: str,
        stdin: str,
        expected_output: str,
    ) -> dict[str, Any]:
        lang_id = LANGUAGE_IDS.get(language)
        if not lang_id:
            return {
                "status": "compile_error",
                "stdout": "",
                "stderr": f"unsupported language: {language}",
                "runtime_ms": 0,
                "memory_kb": 0,
            }

        if self._judge0_unavailable and settings.use_local_runner_fallback:
            return await local_runner.run(language, source_code, stdin, expected_output)

        payload = {
            "language_id": lang_id,
            "source_code": _b64(source_code),
            "stdin": _b64(stdin),
            "expected_output": _b64(expected_output),
            "cpu_time_limit": 5,
            "memory_limit": 128000,
        }

        last_error: Exception | None = None
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(2):
                try:
                    resp = await client.post(
                        f"{self.base_url}/submissions?base64_encoded=true&wait=true",
                        json=payload,
                        headers=self._headers(),
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    self._judge0_unavailable = False
                    return self._normalize(data)
                except (httpx.HTTPError, asyncio.TimeoutError) as exc:
                    last_error = exc
                    await asyncio.sleep(0.3 * (attempt + 1))

        self._judge0_unavailable = True
        if settings.use_local_runner_fallback:
            logger.warning(
                "judge0 unreachable (%s) — falling back to local runner", last_error
            )
            return await local_runner.run(language, source_code, stdin, expected_output)

        return {
            "status": "runtime_error",
            "stdout": "",
            "stderr": f"judge0 unavailable: {last_error}",
            "runtime_ms": 0,
            "memory_kb": 0,
        }

    @staticmethod
    def _normalize(data: dict[str, Any]) -> dict[str, Any]:
        status_id = (data.get("status") or {}).get("id", 0)
        status = STATUS_NORMALIZATION.get(status_id, "wrong_answer")
        time_str = data.get("time") or "0"
        try:
            runtime_ms = int(float(time_str) * 1000)
        except ValueError:
            runtime_ms = 0
        return {
            "status": status,
            "stdout": _b64_decode(data.get("stdout")),
            "stderr": _b64_decode(data.get("stderr")) or _b64_decode(data.get("compile_output")),
            "runtime_ms": runtime_ms,
            "memory_kb": data.get("memory") or 0,
        }


judge0 = Judge0Client()
