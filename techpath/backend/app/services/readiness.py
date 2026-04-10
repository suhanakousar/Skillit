from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.career import JobProfile
from app.models.problem import Problem, Submission
from app.models.project import UserProject
from app.models.user import User

SKILL_EVALUATORS = {
    "dsa": "solved_count",
    "full_stack": "track_progress",
    "system_design": "track_progress",
    "sql": "track_progress",
    "ml": "track_progress",
    "cloud": "track_progress",
    "projects": "projects_count",
    "oop": "track_progress",
    "behavioral": "fixed",
}


async def _solved_count(db: AsyncSession, user_id: UUID, tag: str | None = None) -> int:
    stmt = (
        select(func.count(func.distinct(Problem.id)))
        .join(Submission, Submission.problem_id == Problem.id)
        .where(Submission.user_id == user_id, Submission.status == "accepted")
    )
    if tag:
        stmt = stmt.where(Problem.tags.any(tag))
    return (await db.execute(stmt)).scalar_one() or 0


async def _completed_projects(db: AsyncSession, user_id: UUID) -> int:
    stmt = select(func.count(UserProject.id)).where(
        UserProject.user_id == user_id,
        UserProject.status.in_(("submitted", "completed")),
    )
    return (await db.execute(stmt)).scalar_one() or 0


async def calculate_job_readiness(
    db: AsyncSession,
    user_id: UUID,
    job_profile_id: UUID,
) -> dict:
    job = await db.get(JobProfile, job_profile_id)
    if not job:
        raise ValueError("job profile not found")

    user = await db.get(User, user_id)
    if not user:
        raise ValueError("user not found")

    dsa_solved = await _solved_count(db, user_id)
    projects = await _completed_projects(db, user_id)

    breakdown = []
    totals: list[int] = []

    for skill in job.required_skills:
        area = skill.get("area", "unknown")
        required_pct = int(skill.get("required_percent", 50))
        current_pct = 0
        action = ""

        if area == "dsa":
            target_problems = max(1, required_pct // 2)
            current_pct = min(100, int(dsa_solved * 100 / target_problems))
            action = (
                f"Solve {max(0, target_problems - dsa_solved)} more problems"
                if dsa_solved < target_problems
                else "DSA target met"
            )
        elif area == "projects":
            target_projects = max(1, required_pct // 40)
            current_pct = min(100, int(projects * 100 / target_projects))
            action = (
                f"Ship {max(0, target_projects - projects)} more project(s)"
                if projects < target_projects
                else "Projects target met"
            )
        elif area == "behavioral":
            current_pct = 20
            action = "Practice STAR-format answers in mock interviews"
        else:
            track_tag = area
            solved_here = await _solved_count(db, user_id, tag=track_tag)
            current_pct = min(100, solved_here * 10)
            action = f"Complete the {area.upper()} track"

        gap = max(0, required_pct - current_pct)
        weighted = int(min(current_pct, required_pct) * 100 / required_pct) if required_pct else 0
        totals.append(weighted)

        breakdown.append(
            {
                "area": area,
                "required": required_pct,
                "current": current_pct,
                "gap": gap,
                "action": action,
            }
        )

    overall = int(sum(totals) / len(totals)) if totals else 0
    estimated_weeks = max(1, (100 - overall) // 10)
    gaps_sorted = sorted(breakdown, key=lambda b: b["gap"], reverse=True)
    next_milestone = (
        gaps_sorted[0]["action"] if gaps_sorted and gaps_sorted[0]["gap"] > 0 else "Apply now!"
    )

    return {
        "job_profile_id": job.id,
        "company_name": job.company_name,
        "role_title": job.role_title,
        "overall_readiness": overall,
        "breakdown": breakdown,
        "estimated_weeks_to_ready": estimated_weeks,
        "next_milestone": next_milestone,
    }
