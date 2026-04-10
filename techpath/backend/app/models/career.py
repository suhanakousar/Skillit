import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobProfile(Base):
    __tablename__ = "job_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role_title: Mapped[str] = mapped_column(String(120), nullable=False)
    package_lpa: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    required_skills: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    required_tracks: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), default=list, nullable=False
    )
    difficulty_level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    application_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserJobReadiness(Base):
    __tablename__ = "user_job_readiness"
    __table_args__ = (
        UniqueConstraint("user_id", "job_profile_id", name="uq_user_job_profile"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    job_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("job_profiles.id", ondelete="CASCADE"), nullable=False
    )
    readiness_percent: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    gap_areas_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    last_calculated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    provider: Mapped[str] = mapped_column(String(40), nullable=False)
    related_track_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), default=list, nullable=False
    )
    difficulty: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    exam_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tips_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)


class UserCertification(Base):
    __tablename__ = "user_certifications"
    __table_args__ = (UniqueConstraint("user_id", "cert_id", name="uq_user_cert"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    cert_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("certifications.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), default="planned", nullable=False)
    passed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
