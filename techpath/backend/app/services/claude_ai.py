import json
from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic

from app.config import settings

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic | None:
    global _client
    if _client is None and settings.anthropic_api_key:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


def _fallback(kind: str, context: dict) -> str:
    return (
        f"[{kind} offline — configure ANTHROPIC_API_KEY]\n"
        f"Context: {json.dumps(context, default=str)}"
    )


async def stream_explanation(concept: str, year: int, language: str) -> AsyncIterator[str]:
    client = _get_client()
    prompt = (
        f"Explain '{concept}' to a Year {year} B.Tech CS student in India who prefers {language}. "
        "Use a short real-world story, a simple analogy, then a minimal code example. "
        "Match depth to the year: Year 1 = very simple, Year 4 = technical depth."
    )
    if not client:
        yield _fallback("explanation", {"concept": concept, "year": year, "language": language})
        return

    async with client.messages.stream(
        model=settings.claude_model,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for text in stream.text_stream:
            yield text


async def generate_hint(problem_title: str, description: str, hint_level: int, user_code: str | None) -> str:
    client = _get_client()
    guidance = {
        1: "Give a subtle nudge only. One sentence about where to look. No code.",
        2: "Describe the approach in 2-3 sentences. Name the data structure or pattern. Still no code.",
        3: "Reveal the key insight and pseudocode. Never give the full solution.",
    }[hint_level]
    prompt = (
        f"Problem: {problem_title}\n\n{description}\n\n"
        f"User's current code:\n{user_code or '(empty)'}\n\n"
        f"Task: {guidance}"
    )
    if not client:
        return _fallback("hint", {"problem": problem_title, "level": hint_level})

    msg = await client.messages.create(
        model=settings.claude_model,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text if msg.content else ""


async def review_code(code: str, language: str, problem_title: str | None) -> dict:
    client = _get_client()
    prompt = (
        f"Review this {language} code"
        + (f" for the problem '{problem_title}'" if problem_title else "")
        + ". Return STRICT JSON with keys: correctness (string), time_complexity (string), "
        "space_complexity (string), style_score (0-10), suggestions (array of strings).\n\n"
        f"Code:\n```{language}\n{code}\n```"
    )
    if not client:
        return {
            "correctness": "offline",
            "time_complexity": "unknown",
            "space_complexity": "unknown",
            "style_score": 0,
            "suggestions": ["Configure ANTHROPIC_API_KEY to enable AI review."],
        }

    msg = await client.messages.create(
        model=settings.claude_model,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text if msg.content else "{}"
    try:
        start = text.find("{")
        end = text.rfind("}")
        return json.loads(text[start : end + 1])
    except (json.JSONDecodeError, ValueError):
        return {
            "correctness": "unknown",
            "time_complexity": "unknown",
            "space_complexity": "unknown",
            "style_score": 0,
            "suggestions": [text[:500]],
        }


async def stream_story_lesson(topic: str, year: int, language: str, goal: str) -> AsyncIterator[str]:
    client = _get_client()
    prompt = (
        f"Generate a story-mode lesson for TechPath on '{topic}'. "
        f"Student: Year {year} B.Tech CS, prefers {language}, goal = {goal}. "
        "Return STRICT JSON with keys: title, hook_story, aha_moment, concept_explained, "
        "visual_description, code_walkthrough (array of {step, comment, code}), "
        "common_mistakes (array), quiz (array of {question, options, correct, explanation}), "
        "next_topic, xp_reward."
    )
    if not client:
        yield _fallback("story_lesson", {"topic": topic, "year": year})
        return

    async with client.messages.stream(
        model=settings.claude_model,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for text in stream.text_stream:
            yield text
