"""initial schema

Revision ID: 20260101_0001
Revises:
Create Date: 2026-01-01 00:00:00

Creates every TechPath table in one revision. Matches the canonical schema in
db/schema.sql and the SQLAlchemy models in app/models/.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260101_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # -------------------------------------------------------------- users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("year", sa.SmallInteger, nullable=False),
        sa.Column("branch", sa.String(20), nullable=False),
        sa.Column("goal", sa.String(20), nullable=False),
        sa.Column("preferred_language", sa.String(20), nullable=False, server_default="python"),
        sa.Column("college", sa.String(120)),
        sa.Column("xp_total", sa.Integer, nullable=False, server_default="0"),
        sa.Column("streak_current", sa.Integer, nullable=False, server_default="0"),
        sa.Column("streak_max", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_active_date", sa.Date),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("year BETWEEN 1 AND 4"),
        sa.CheckConstraint("branch IN ('CSE','AIDS','AIML','IoT','ECE','OTHER')"),
        sa.CheckConstraint("goal IN ('job','gate','startup','research')"),
    )
    op.create_index("idx_users_email", "users", ["email"])
    op.create_index("idx_users_college", "users", ["college"])
    op.create_index("idx_users_xp", "users", [sa.text("xp_total DESC")])

    # -------------------------------------------------------------- tracks
    op.create_table(
        "tracks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("domain", sa.String(40), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("year_recommended", sa.SmallInteger, nullable=False),
        sa.Column("order_index", sa.Integer, nullable=False, server_default="0"),
        sa.Column("prerequisite_track_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False, server_default="{}"),
        sa.Column("total_xp", sa.Integer, nullable=False, server_default="0"),
        sa.Column("estimated_hours", sa.Integer, nullable=False, server_default="0"),
        sa.Column("icon", sa.String(40)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("year_recommended BETWEEN 1 AND 4"),
    )
    op.create_index("idx_tracks_domain", "tracks", ["domain"])
    op.create_index("idx_tracks_year", "tracks", ["year_recommended"])

    # -------------------------------------------------------------- lessons
    op.create_table(
        "lessons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("track_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("content_json", postgresql.JSONB, nullable=False),
        sa.Column("xp_reward", sa.Integer, nullable=False, server_default="10"),
        sa.Column("order_index", sa.Integer, nullable=False, server_default="0"),
        sa.Column("duration_minutes", sa.Integer, nullable=False, server_default="10"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("type IN ('story','interactive','codealong')"),
    )
    op.create_index("idx_lessons_track", "lessons", ["track_id"])

    # -------------------------------------------------------------- user_progress
    op.create_table(
        "user_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("track_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id", ondelete="CASCADE")),
        sa.Column("status", sa.String(20), nullable=False, server_default="not_started"),
        sa.Column("score", sa.Integer),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_progress_user_lesson"),
        sa.CheckConstraint("status IN ('not_started','in_progress','completed')"),
    )
    op.create_index("idx_progress_user", "user_progress", ["user_id"])
    op.create_index("idx_progress_track", "user_progress", ["user_id", "track_id"])

    # -------------------------------------------------------------- problems
    op.create_table(
        "problems",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("track_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tracks.id", ondelete="SET NULL")),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("difficulty", sa.SmallInteger, nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("starter_code_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("test_cases_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("examples_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("constraints_text", sa.Text),
        sa.Column("xp_reward", sa.Integer, nullable=False, server_default="20"),
        sa.Column("hints_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("solution_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("difficulty BETWEEN 1 AND 5"),
    )
    op.create_index("idx_problems_difficulty", "problems", ["difficulty"])
    op.create_index("idx_problems_tags", "problems", ["tags"], postgresql_using="gin")
    op.create_index("idx_problems_track", "problems", ["track_id"])

    # -------------------------------------------------------------- submissions
    op.create_table(
        "submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("problem_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False),
        sa.Column("language", sa.String(20), nullable=False),
        sa.Column("code", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("runtime_ms", sa.Integer),
        sa.Column("memory_kb", sa.Integer),
        sa.Column("percentile", sa.Numeric(5, 2)),
        sa.Column("test_results_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "status IN ('accepted','wrong_answer','tle','runtime_error','compile_error','pending')"
        ),
    )
    op.create_index("idx_submissions_user_problem", "submissions", ["user_id", "problem_id"])
    op.create_index("idx_submissions_status", "submissions", ["status"])
    op.create_index("idx_submissions_submitted", "submissions", [sa.text("submitted_at DESC")])

    # -------------------------------------------------------------- projects
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("track_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tracks.id", ondelete="SET NULL")),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("tech_stack", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("milestones_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("year_recommended", sa.SmallInteger),
        sa.Column("xp_total", sa.Integer, nullable=False, server_default="100"),
        sa.Column("repo_template_url", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("year_recommended BETWEEN 1 AND 4"),
    )
    op.create_index("idx_projects_year", "projects", ["year_recommended"])

    op.create_table(
        "user_projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="in_progress"),
        sa.Column("milestones_completed", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("github_url", sa.String(500)),
        sa.Column("live_url", sa.String(500)),
        sa.Column("submitted_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "project_id", name="uq_user_project"),
        sa.CheckConstraint("status IN ('in_progress','submitted','reviewed','completed')"),
    )

    # -------------------------------------------------------------- badges
    op.create_table(
        "badges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("slug", sa.String(60), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("icon", sa.String(60)),
        sa.Column("condition_json", postgresql.JSONB, nullable=False),
        sa.Column("xp_bonus", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "user_badges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("badge_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("badges.id", ondelete="CASCADE"), nullable=False),
        sa.Column("earned_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )
    op.create_index("idx_user_badges_user", "user_badges", ["user_id"])

    # -------------------------------------------------------------- contests
    op.create_table(
        "contests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("problem_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_contests_start", "contests", [sa.text("start_time DESC")])

    op.create_table(
        "contest_submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("contest_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("problem_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("submissions.id", ondelete="SET NULL")),
        sa.Column("points", sa.Integer, nullable=False, server_default="0"),
        sa.Column("time_taken_seconds", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_contest_subs_contest", "contest_submissions", ["contest_id", sa.text("points DESC")])

    # -------------------------------------------------------------- career
    op.create_table(
        "job_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("company_name", sa.String(120), nullable=False),
        sa.Column("role_title", sa.String(120), nullable=False),
        sa.Column("package_lpa", sa.Numeric(6, 2)),
        sa.Column("required_skills", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("required_tracks", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False, server_default="{}"),
        sa.Column("difficulty_level", sa.SmallInteger, nullable=False),
        sa.Column("application_url", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("difficulty_level BETWEEN 1 AND 5"),
    )

    op.create_table(
        "user_job_readiness",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("job_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("readiness_percent", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("gap_areas_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("last_calculated", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "job_profile_id", name="uq_user_job_profile"),
        sa.CheckConstraint("readiness_percent BETWEEN 0 AND 100"),
    )

    op.create_table(
        "certifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("provider", sa.String(40), nullable=False),
        sa.Column("related_track_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False, server_default="{}"),
        sa.Column("difficulty", sa.SmallInteger, nullable=False),
        sa.Column("exam_url", sa.String(500)),
        sa.Column("tips_json", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.CheckConstraint("difficulty BETWEEN 1 AND 5"),
    )

    op.create_table(
        "user_certifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cert_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("certifications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="planned"),
        sa.Column("passed_at", sa.DateTime(timezone=True)),
        sa.Column("credential_url", sa.String(500)),
        sa.UniqueConstraint("user_id", "cert_id", name="uq_user_cert"),
        sa.CheckConstraint("status IN ('planned','in_progress','passed')"),
    )

    # -------------------------------------------------------------- roadmap
    op.create_table(
        "roadmap_nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("year", sa.SmallInteger, nullable=False),
        sa.Column("domain", sa.String(40), nullable=False),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("prerequisite_node_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False, server_default="{}"),
        sa.Column("track_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tracks.id", ondelete="SET NULL")),
        sa.Column("position_x", sa.Integer, nullable=False, server_default="0"),
        sa.Column("position_y", sa.Integer, nullable=False, server_default="0"),
        sa.CheckConstraint("year BETWEEN 1 AND 4"),
    )
    op.create_index("idx_roadmap_year", "roadmap_nodes", ["year"])


def downgrade() -> None:
    for table in [
        "roadmap_nodes",
        "user_certifications",
        "certifications",
        "user_job_readiness",
        "job_profiles",
        "contest_submissions",
        "contests",
        "user_badges",
        "badges",
        "user_projects",
        "projects",
        "submissions",
        "problems",
        "user_progress",
        "lessons",
        "tracks",
        "users",
    ]:
        op.drop_table(table)
