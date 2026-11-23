import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AuthMode, ElectionStatus


class Election(Base):
    """Configurable election container (table: elections)."""

    __tablename__ = "elections"
    __table_args__ = (
        CheckConstraint("end_time > start_time", name="ck_elections_end_after_start"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("organizers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    auth_mode: Mapped[AuthMode] = mapped_column(
        SAEnum(AuthMode, name="auth_mode", native_enum=False),
        nullable=False,
        default=AuthMode.CSV_ROSTER,
    )
    status: Mapped[ElectionStatus] = mapped_column(
        SAEnum(ElectionStatus, name="election_status", native_enum=False),
        nullable=False,
        default=ElectionStatus.DRAFT,
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    organizer: Mapped["ElectionOrganizer"] = relationship(  # noqa: F821
        back_populates="elections"
    )
    eligible_voters: Mapped[list["VoterEligibility"]] = relationship(  # noqa: F821
        back_populates="election",
        cascade="all, delete-orphan",
    )
    questions: Mapped[list["BallotQuestion"]] = relationship(  # noqa: F821
        back_populates="election",
        cascade="all, delete-orphan",
    )
