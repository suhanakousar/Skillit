"""Seed the TechPath database with starter content.

Usage:
    python -m app.seed
"""
import asyncio
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select

from app.config import settings
from app.content.lessons_data import LESSONS_BY_TRACK
from app.content.problems_data import PROBLEMS
from app.content.python_roadmap_data import (
    PYTHON_ROADMAP_LESSONS,
    PYTHON_ROADMAP_PROBLEMS,
    PYTHON_ROADMAP_PROJECTS,
    PYTHON_ROADMAP_TRACKS,
)
from app.database import AsyncSessionLocal, Base, engine
from app.models.badge import Badge, UserBadge
from app.models.career import JobProfile
from app.models.contest import Contest
from app.models.lesson import Lesson, UserProgress
from app.models.problem import Problem, Submission
from app.models.project import Project
from app.models.roadmap import RoadmapNode
from app.models.track import Track
from app.models.user import User
from app.security import hash_password

# -----------------------------------------------------------------------------
# TRACKS (spans 4 years across 6 domains)
# -----------------------------------------------------------------------------
TRACKS = [
    # Year 1
    ("Python Basics", "python-basics", "Programming", 1, "Variables, loops, functions, lists, dicts. Your first 'aha' moments in code.", 30, 500),
    ("C Fundamentals", "c-fundamentals", "Programming", 1, "Pointers, memory, structs. The closest you get to the machine.", 30, 600),
    ("Math for CS", "math-for-cs", "Math", 1, "Sets, logic, combinatorics, graph theory basics.", 20, 400),
    ("DSA Foundations", "dsa-foundations", "DSA", 1, "Arrays, strings, searching, sorting. The bedrock of every interview.", 40, 800),
    ("Linux & Terminal", "linux-terminal", "DevOps", 1, "Bash, files, permissions, pipes. Stop being scared of the black screen.", 15, 300),
    ("Web Basics", "web-basics", "Web", 1, "HTML5, CSS3, Flexbox, Grid. Ship your first landing page.", 20, 400),
    # Year 2
    ("DSA Intermediate", "dsa-intermediate", "DSA", 2, "Trees, graphs, hashing, sliding window. Interview-grade problem patterns.", 60, 1200),
    ("Full Stack: React", "full-stack-react", "Web", 2, "Components, hooks, state, routing. Build SPAs the modern way.", 50, 1000),
    ("Full Stack: Node", "full-stack-node", "Web", 2, "Express, REST APIs, middleware, JWT auth.", 40, 800),
    ("DBMS + SQL", "dbms-sql", "Database", 2, "ER models, normalization, joins, indexes, transactions.", 35, 700),
    ("Operating Systems", "operating-systems", "Systems", 2, "Processes, threads, memory management, scheduling.", 40, 800),
    ("Computer Networks", "computer-networks", "Systems", 2, "TCP/IP, HTTP, DNS, sockets. How the internet actually works.", 35, 600),
    # Year 3
    ("DSA Advanced", "dsa-advanced", "DSA", 3, "DP, greedy, backtracking, segment trees, tries.", 80, 1500),
    ("System Design Intro", "system-design-intro", "Systems", 3, "Scalability, caching, load balancing, DB sharding basics.", 50, 1000),
    ("ML Fundamentals", "ml-fundamentals", "ML", 3, "Regression, classification, trees, evaluation metrics.", 60, 1100),
    ("DevOps: Docker + CI/CD", "devops", "DevOps", 3, "Containers, compose, GitHub Actions, automated deploys.", 35, 700),
    ("Cloud: AWS Basics", "aws-basics", "Cloud", 3, "EC2, S3, Lambda, RDS. The core AWS primitives.", 40, 800),
    # Year 4
    ("Deep Learning", "deep-learning", "ML", 4, "Neural nets, CNNs, RNNs, transformers.", 80, 1500),
    ("System Design Advanced", "system-design-advanced", "Systems", 4, "Distributed systems, consensus, CAP, real-world architectures.", 70, 1400),
    ("Interview Prep", "interview-prep", "Career", 4, "Mock interviews, behavioral rounds, salary negotiation.", 40, 800),
    # Python: Beginner-to-Pro roadmap (6 stages, 4 Stage-5 specializations)
    *PYTHON_ROADMAP_TRACKS,
]

# -----------------------------------------------------------------------------
# PROJECTS (year-wise builds)
# -----------------------------------------------------------------------------
PROJECTS_DATA = [
    (1, "CLI Todo App", "cli-todo", "Build a command-line todo list with add/list/done/delete. Persist to JSON.", ["python"], 100),
    (1, "ATM Simulator", "atm-sim", "Simulate ATM: PIN auth, balance, deposit, withdraw, transaction history.", ["python"], 120),
    (1, "Grade Manager", "grade-manager", "Student grade tracker: CRUD, averages, rank lists, CSV export.", ["python"], 100),
    (2, "Chat App (Sockets)", "chat-sockets", "Real-time chat with Python sockets. Multiple rooms, usernames.", ["python", "sockets"], 200),
    (2, "Blog REST API", "blog-rest-api", "CRUD posts, auth with JWT, PostgreSQL, FastAPI backend.", ["fastapi", "postgres"], 250),
    (2, "Weather Dashboard", "weather-dashboard", "React frontend consuming a public weather API. Dark mode, search history.", ["react", "tailwind"], 200),
    (2, "E-commerce Mini", "ecommerce-mini", "Product list, cart, checkout. Full stack with React + Node.", ["react", "express"], 280),
    (3, "Microservices E-Commerce", "ms-ecommerce", "Users, products, orders as separate services. Docker compose.", ["fastapi", "docker", "postgres"], 400),
    (3, "ML Price Predictor", "ml-price-predictor", "Train a regression model on housing data. Deploy as a REST endpoint.", ["sklearn", "fastapi"], 350),
    (3, "Image Classifier", "image-classifier", "CNN for 10-class image classification. Gradio demo.", ["pytorch", "gradio"], 400),
    (4, "Full SaaS App", "saas-capstone", "End-to-end SaaS: auth, payments, dashboard, email. Deployed to production.", ["nextjs", "stripe", "postgres"], 600),
    (4, "AI Chatbot Agent", "ai-chatbot-agent", "Claude-powered agent with tool use. Multi-turn memory. Streaming UI.", ["claude", "react"], 500),
    (4, "Recommendation System", "recommender-sys", "Collaborative filtering recommender with a web demo.", ["pytorch", "fastapi"], 500),
]

PROJECT_MILESTONES = [
    {"index": 0, "title": "Setup", "xp": 20},
    {"index": 1, "title": "Core feature", "xp": 30},
    {"index": 2, "title": "Extend", "xp": 40},
    {"index": 3, "title": "Auth", "xp": 50},
    {"index": 4, "title": "Deploy", "xp": 100},
]

# -----------------------------------------------------------------------------
# BADGES (20)
# -----------------------------------------------------------------------------
BADGES = [
    ("first-blood", "First Blood", "Solve your first problem.", "sword", {"type": "first_submission"}, 10),
    ("hello-world", "Hello World", "Complete your first lesson.", "wave", {"type": "first_lesson"}, 10),
    ("streak-starter", "Streak Starter", "Reach a 7-day streak.", "flame", {"type": "streak", "target": 7}, 50),
    ("hot-streak", "Hot Streak", "Reach a 30-day streak.", "fire", {"type": "streak", "target": 30}, 200),
    ("array-master", "Array Master", "Solve 10 array problems.", "grid", {"type": "tag_solved", "tag": "arrays", "target": 10}, 100),
    ("tree-whisperer", "Tree Whisperer", "Solve 10 tree problems.", "tree", {"type": "tag_solved", "tag": "trees", "target": 10}, 100),
    ("graph-guru", "Graph Guru", "Solve 10 graph problems.", "network", {"type": "tag_solved", "tag": "graphs", "target": 10}, 100),
    ("dp-slayer", "DP Slayer", "Solve 10 DP problems.", "brain", {"type": "tag_solved", "tag": "dp", "target": 10}, 150),
    ("string-surgeon", "String Surgeon", "Solve 10 string problems.", "text", {"type": "tag_solved", "tag": "strings", "target": 10}, 100),
    ("easy-10", "Warming Up", "Solve 10 easy problems.", "spark", {"type": "difficulty_solved", "difficulty": 1, "target": 10}, 50),
    ("medium-10", "Rising Star", "Solve 10 medium problems.", "star", {"type": "difficulty_solved", "difficulty": 3, "target": 10}, 150),
    ("hard-5", "Fearless", "Solve 5 hard problems.", "shield", {"type": "difficulty_solved", "difficulty": 5, "target": 5}, 300),
    ("centurion", "Centurion", "Solve 100 problems.", "helmet", {"type": "problems_solved", "target": 100}, 500),
    ("legend", "Legend", "Reach 10,000 XP.", "crown", {"type": "xp_total", "target": 10000}, 1000),
    ("apprentice", "Apprentice", "Reach 500 XP.", "book", {"type": "xp_total", "target": 500}, 25),
    ("scholar", "Scholar", "Reach 2,000 XP.", "graduation", {"type": "xp_total", "target": 2000}, 100),
    ("expert", "Expert", "Reach 5,000 XP.", "medal", {"type": "xp_total", "target": 5000}, 250),
    ("night-owl", "Night Owl", "Solve 20 problems total.", "moon", {"type": "problems_solved", "target": 20}, 50),
    ("speedrun", "Speedrun", "Solve 50 problems total.", "lightning", {"type": "problems_solved", "target": 50}, 150),
    ("grinder", "The Grinder", "Solve 25 problems.", "weight", {"type": "problems_solved", "target": 25}, 75),
]

# -----------------------------------------------------------------------------
# JOB PROFILES (6 companies)
# -----------------------------------------------------------------------------
JOB_PROFILES = [
    ("amazon-sde-1", "Amazon", "SDE-1", 44.0, 4, [
        {"area": "dsa", "required_percent": 80},
        {"area": "system_design", "required_percent": 50},
        {"area": "projects", "required_percent": 60},
        {"area": "oop", "required_percent": 60},
        {"area": "behavioral", "required_percent": 50},
    ]),
    ("google-swe", "Google", "SWE L3", 60.0, 5, [
        {"area": "dsa", "required_percent": 90},
        {"area": "system_design", "required_percent": 70},
        {"area": "behavioral", "required_percent": 60},
    ]),
    ("microsoft-swe", "Microsoft", "SWE", 42.0, 4, [
        {"area": "dsa", "required_percent": 75},
        {"area": "full_stack", "required_percent": 60},
        {"area": "cloud", "required_percent": 50},
        {"area": "projects", "required_percent": 60},
    ]),
    ("infosys-se", "Infosys/TCS/Wipro", "Systems Engineer", 7.0, 2, [
        {"area": "dsa", "required_percent": 40},
        {"area": "sql", "required_percent": 50},
        {"area": "projects", "required_percent": 40},
    ]),
    ("startup-fullstack", "Startup (Seed)", "Full Stack Engineer", 16.0, 3, [
        {"area": "full_stack", "required_percent": 80},
        {"area": "projects", "required_percent": 80},
        {"area": "behavioral", "required_percent": 40},
    ]),
    ("ml-engineer", "AI Startup", "ML Engineer", 25.0, 4, [
        {"area": "ml", "required_percent": 70},
        {"area": "dsa", "required_percent": 50},
        {"area": "projects", "required_percent": 60},
    ]),
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        existing = (await db.execute(select(Track))).scalars().first()
        if existing:
            print("Seed data already present. Skipping.")
            return

        tracks_by_slug: dict[str, Track] = {}
        for i, (name, slug, domain, year, desc, hours, xp) in enumerate(TRACKS):
            t = Track(
                name=name,
                slug=slug,
                domain=domain,
                description=desc,
                year_recommended=year,
                order_index=i,
                total_xp=xp,
                estimated_hours=hours,
                icon=domain.lower(),
            )
            db.add(t)
            tracks_by_slug[slug] = t
        await db.flush()

        lesson_count = 0
        all_lessons_by_track: dict[str, list[dict]] = {}
        for track_slug, lessons in LESSONS_BY_TRACK.items():
            all_lessons_by_track.setdefault(track_slug, []).extend(lessons)
        for track_slug, lessons in PYTHON_ROADMAP_LESSONS.items():
            all_lessons_by_track.setdefault(track_slug, []).extend(lessons)

        for track_slug, lessons in all_lessons_by_track.items():
            track = tracks_by_slug.get(track_slug)
            if not track:
                continue
            for i, lesson in enumerate(lessons):
                db.add(
                    Lesson(
                        track_id=track.id,
                        title=lesson["title"],
                        type=lesson["type"],
                        content_json=lesson["content_json"],
                        xp_reward=lesson["xp_reward"],
                        order_index=i,
                        duration_minutes=lesson["duration_minutes"],
                    )
                )
                lesson_count += 1

        dsa_track = tracks_by_slug["dsa-foundations"]
        all_problems = list(PROBLEMS) + list(PYTHON_ROADMAP_PROBLEMS)
        for p in all_problems:
            target_track = tracks_by_slug.get(p.get("track_slug", ""), dsa_track)
            db.add(
                Problem(
                    track_id=target_track.id,
                    title=p["title"],
                    slug=p["slug"],
                    description=p["description"],
                    difficulty=p["difficulty"],
                    tags=p["tags"],
                    xp_reward=p["xp_reward"],
                    examples_json=p.get("examples_json", []),
                    test_cases_json=p.get("test_cases_json", []),
                    starter_code_json=p.get("starter_code_json", {}),
                    hints_json=p.get("hints_json", []),
                    constraints_text=p.get("constraints_text"),
                )
            )

        for year, title, slug, desc, stack, xp in list(PROJECTS_DATA) + list(PYTHON_ROADMAP_PROJECTS):
            db.add(
                Project(
                    title=title,
                    slug=slug,
                    description=desc,
                    tech_stack=stack,
                    milestones_json=PROJECT_MILESTONES,
                    year_recommended=year,
                    xp_total=xp,
                )
            )

        for slug, name, desc, icon, cond, bonus in BADGES:
            db.add(
                Badge(
                    slug=slug,
                    name=name,
                    description=desc,
                    icon=icon,
                    condition_json=cond,
                    xp_bonus=bonus,
                )
            )

        for slug, company, role, lpa, difficulty, skills in JOB_PROFILES:
            db.add(
                JobProfile(
                    slug=slug,
                    company_name=company,
                    role_title=role,
                    package_lpa=lpa,
                    difficulty_level=difficulty,
                    required_skills=skills,
                )
            )

        for i, (name, slug, domain, year, _desc, _h, _x) in enumerate(TRACKS):
            track = tracks_by_slug[slug]
            db.add(
                RoadmapNode(
                    year=year,
                    domain=domain,
                    title=name,
                    description=f"Part of Year {year} curriculum",
                    track_id=track.id,
                    position_x=(i % 6) * 200,
                    position_y=(year - 1) * 180,
                )
            )

        now = datetime.now(timezone.utc)
        db.add(
            Contest(
                title="TechPath Weekly #1",
                description="Welcome contest. 3 problems, 90 minutes.",
                start_time=now,
                end_time=now + timedelta(minutes=90),
                problem_ids=[],
                is_active=True,
            )
        )

        await db.flush()

        demo_user = None
        if settings.seed_demo_user:
            demo_user = User(
                name="Demo Student",
                email=settings.demo_email,
                password_hash=hash_password(settings.demo_password),
                year=2,
                branch="CSE",
                goal="job",
                preferred_language="python",
                college="KL University",
                xp_total=340,
                streak_current=5,
                streak_max=12,
                last_active_date=date.today(),
            )
            db.add(demo_user)
            await db.flush()

            seeded_lessons = (await db.execute(select(Lesson).limit(4))).scalars().all()
            for lesson in seeded_lessons:
                db.add(
                    UserProgress(
                        user_id=demo_user.id,
                        track_id=lesson.track_id,
                        lesson_id=lesson.id,
                        status="completed",
                        score=100,
                        completed_at=datetime.now(timezone.utc),
                    )
                )

            easy_problems = (
                await db.execute(
                    select(Problem).where(Problem.difficulty <= 2).limit(5)
                )
            ).scalars().all()
            for problem in easy_problems:
                db.add(
                    Submission(
                        user_id=demo_user.id,
                        problem_id=problem.id,
                        language="python",
                        code="# demo solution\nprint('ok')\n",
                        status="accepted",
                        runtime_ms=42,
                        memory_kb=1024,
                        test_results_json=[],
                    )
                )

            first_blood = (
                await db.execute(select(Badge).where(Badge.slug == "first-blood"))
            ).scalar_one_or_none()
            hello_world = (
                await db.execute(select(Badge).where(Badge.slug == "hello-world"))
            ).scalar_one_or_none()
            apprentice = (
                await db.execute(select(Badge).where(Badge.slug == "apprentice"))
            ).scalar_one_or_none()
            for badge in filter(None, [first_blood, hello_world, apprentice]):
                db.add(UserBadge(user_id=demo_user.id, badge_id=badge.id))

        await db.commit()
        total_problems = len(PROBLEMS) + len(PYTHON_ROADMAP_PROBLEMS)
        total_projects = len(PROJECTS_DATA) + len(PYTHON_ROADMAP_PROJECTS)
        summary = (
            f"Seeded TechPath: {len(TRACKS)} tracks, {lesson_count} lessons, "
            f"{total_problems} problems, {total_projects} projects, "
            f"{len(BADGES)} badges, {len(JOB_PROFILES)} job profiles."
        )
        if demo_user:
            summary += (
                f"\nDemo account: {settings.demo_email} / {settings.demo_password}"
            )
        print(summary)


if __name__ == "__main__":
    asyncio.run(seed())
