import uuid
from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ElectionState


class Election(Base):
    """Timestamp-driven election lifecycle container (table: elections)."""

    __tablename__ = "elections"
    __table_args__ = (
        CheckConstraint("end_time > start_time", name="ck_elections_end_after_start"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    organizer: Mapped["User"] = relationship(  # noqa: F821
        back_populates="elections"
    )
    eligible_voters: Mapped[list["VoterEligibility"]] = relationship(  # noqa: F821
        back_populates="election",
        cascade="all, delete-orphan",
    )
    questions: Mapped[list["BallotQuestion"]] = relationship(  # noqa: F821
        back_populates="election",
        cascade="all, delete-orphan",
        order_by="BallotQuestion.display_order",
    )

    def get_state(self, now: datetime | None = None) -> ElectionState:
        """Derive election lifecycle state deterministically from timestamps."""
        current = now or datetime.now(UTC)
        if self.cancelled_at is not None:
            return ElectionState.CANCELLED
        if self.published_at is None:
            return ElectionState.DRAFT
        start = self.start_time if self.start_time.tzinfo else self.start_time.replace(tzinfo=UTC)
        end = self.end_time if self.end_time.tzinfo else self.end_time.replace(tzinfo=UTC)
        if current < start:
            return ElectionState.UPCOMING
        if current < end:
            return ElectionState.ACTIVE
        return ElectionState.CLOSED

    def is_open(self, now: datetime | None = None) -> bool:
        """Return True iff the election is currently accepting ballots."""
        return self.get_state(now) == ElectionState.ACTIVE

    def is_editable(self) -> bool:
        """Return True iff the election is still an unpublished, uncancelled draft."""
        return self.published_at is None and self.cancelled_at is None
