"""Local in-process code runner used as a fallback when Judge0 is unavailable.

Safe-enough for local development and single-user demos. For production with
untrusted code you MUST use a real sandbox (Judge0, gVisor, Firecracker).

Supports:
- Python (always — the backend's own interpreter)
- JavaScript (if `node` is on PATH)
- C++ (if `g++` is on PATH)
- C (if `gcc` is on PATH)

Returns the same shape as Judge0Client.submit so callers don't care which
backend ran the code.
"""
import asyncio
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

TIMEOUT_SECONDS = 5
MEMORY_LIMIT_MB = 128


def _normalize(text: str) -> str:
    """Collapse trailing whitespace per line and trim final newlines."""
    return "\n".join(line.rstrip() for line in text.splitlines()).rstrip("\n")


async def _run_subprocess(
    cmd: list[str],
    stdin: str,
    cwd: str,
    timeout: float = TIMEOUT_SECONDS,
) -> tuple[str, str, int, int]:
    """Run a subprocess and return (stdout, stderr, exit_code, runtime_ms)."""
    start = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )
    except FileNotFoundError as exc:
        return "", f"compiler/runtime not found: {exc}", -1, 0

    try:
        stdout_b, stderr_b = await asyncio.wait_for(
            proc.communicate(stdin.encode() if stdin else b""),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return "", "time limit exceeded", -2, int((time.monotonic() - start) * 1000)

    runtime_ms = int((time.monotonic() - start) * 1000)
    return (
        stdout_b.decode(errors="replace"),
        stderr_b.decode(errors="replace"),
        proc.returncode or 0,
        runtime_ms,
    )


async def _run_python(source: str, stdin: str, workdir: Path) -> dict:
    src = workdir / "main.py"
    src.write_text(source, encoding="utf-8")
    stdout, stderr, code, rt = await _run_subprocess(
        [sys.executable, "-I", str(src)],
        stdin,
        str(workdir),
    )
    return {"stdout": stdout, "stderr": stderr, "exit_code": code, "runtime_ms": rt}


async def _run_node(source: str, stdin: str, workdir: Path) -> dict:
    if not shutil.which("node"):
        return {
            "stdout": "",
            "stderr": "node runtime not installed in backend",
            "exit_code": -1,
            "runtime_ms": 0,
        }
    src = workdir / "main.js"
    src.write_text(source, encoding="utf-8")
    stdout, stderr, code, rt = await _run_subprocess(["node", str(src)], stdin, str(workdir))
    return {"stdout": stdout, "stderr": stderr, "exit_code": code, "runtime_ms": rt}


async def _run_cpp(source: str, stdin: str, workdir: Path) -> dict:
    if not shutil.which("g++"):
        return {
            "stdout": "",
            "stderr": "g++ compiler not installed in backend",
            "exit_code": -1,
            "runtime_ms": 0,
        }
    src = workdir / "main.cpp"
    exe = workdir / ("main.exe" if os.name == "nt" else "main")
    src.write_text(source, encoding="utf-8")

    _, build_err, build_code, _ = await _run_subprocess(
        ["g++", "-O2", "-std=c++17", str(src), "-o", str(exe)],
        "",
        str(workdir),
        timeout=15,
    )
    if build_code != 0:
        return {"stdout": "", "stderr": build_err or "compile error", "exit_code": -3, "runtime_ms": 0}

    stdout, stderr, code, rt = await _run_subprocess([str(exe)], stdin, str(workdir))
    return {"stdout": stdout, "stderr": stderr, "exit_code": code, "runtime_ms": rt}


async def _run_c(source: str, stdin: str, workdir: Path) -> dict:
    if not shutil.which("gcc"):
        return {
            "stdout": "",
            "stderr": "gcc compiler not installed in backend",
            "exit_code": -1,
            "runtime_ms": 0,
        }
    src = workdir / "main.c"
    exe = workdir / ("main.exe" if os.name == "nt" else "main")
    src.write_text(source, encoding="utf-8")

    _, build_err, build_code, _ = await _run_subprocess(
        ["gcc", "-O2", str(src), "-o", str(exe)],
        "",
        str(workdir),
        timeout=15,
    )
    if build_code != 0:
        return {"stdout": "", "stderr": build_err, "exit_code": -3, "runtime_ms": 0}

    stdout, stderr, code, rt = await _run_subprocess([str(exe)], stdin, str(workdir))
    return {"stdout": stdout, "stderr": stderr, "exit_code": code, "runtime_ms": rt}


RUNNERS = {
    "python": _run_python,
    "javascript": _run_node,
    "cpp": _run_cpp,
    "c": _run_c,
}


async def run(language: str, source: str, stdin: str, expected: str) -> dict:
    """Execute code locally and compare output to expected.

    Returns a dict matching the Judge0Client response shape:
        {status, stdout, stderr, runtime_ms, memory_kb}
    """
    runner = RUNNERS.get(language)
    if not runner:
        return {
            "status": "compile_error",
            "stdout": "",
            "stderr": f"local runner does not support {language}",
            "runtime_ms": 0,
            "memory_kb": 0,
        }

    with tempfile.TemporaryDirectory(prefix="techpath_") as tmp:
        result = await runner(source, stdin, Path(tmp))

    exit_code = result["exit_code"]
    stdout = result["stdout"]
    stderr = result["stderr"]

    if exit_code == -2:
        status = "tle"
    elif exit_code == -3:
        status = "compile_error"
    elif exit_code < 0:
        status = "runtime_error"
    elif exit_code != 0:
        status = "runtime_error"
    elif _normalize(stdout) == _normalize(expected):
        status = "accepted"
    else:
        status = "wrong_answer"

    return {
        "status": status,
        "stdout": stdout,
        "stderr": stderr,
        "runtime_ms": result["runtime_ms"],
        "memory_kb": 0,
    }
