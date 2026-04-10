import pytest

from app.services import local_runner


@pytest.mark.asyncio
async def test_python_accepted():
    source = "print(int(input()) * 2)\n"
    result = await local_runner.run("python", source, "21\n", "42")
    assert result["status"] == "accepted"
    assert result["stdout"].strip() == "42"


@pytest.mark.asyncio
async def test_python_wrong_answer():
    source = "print('no')\n"
    result = await local_runner.run("python", source, "", "yes")
    assert result["status"] == "wrong_answer"


@pytest.mark.asyncio
async def test_python_runtime_error():
    source = "raise RuntimeError('boom')\n"
    result = await local_runner.run("python", source, "", "")
    assert result["status"] == "runtime_error"
    assert "boom" in result["stderr"] or "RuntimeError" in result["stderr"]


@pytest.mark.asyncio
async def test_python_tle():
    source = "while True: pass\n"
    result = await local_runner.run("python", source, "", "")
    assert result["status"] == "tle"


@pytest.mark.asyncio
async def test_unsupported_language_returns_compile_error():
    result = await local_runner.run("brainfuck", "+++", "", "")
    assert result["status"] == "compile_error"
    assert "does not support" in result["stderr"]


@pytest.mark.asyncio
async def test_whitespace_tolerance_in_comparison():
    source = "print('  hello  ')\nprint('world')\n"
    result = await local_runner.run("python", source, "", "hello\nworld")
    assert result["status"] == "accepted"
