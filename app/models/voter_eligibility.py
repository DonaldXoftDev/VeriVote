import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.election import Election


class VoterEligibility(Base):
    """Accreditation roll air-gapped from anonymous ballots (table: voter_eligibility).

    SECURITY INVARIANT: Never add a foreign key or direct link between this table
    and `anonymous_ballots` or `ballot_choices`.
    """

    __tablename__ = "voter_eligibility"
    __table_args__ = (
        UniqueConstraint("election_id", "email", name="uq_voter_election_email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("elections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    voter_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    otp_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    otp_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    otp_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    voted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    election: Mapped["Election"] = relationship(  # noqa: F821
        back_populates="eligible_voters"
    )

    def has_voted(self) -> bool:
        """Return True iff this accredited voter has already cast their ballot."""
        return self.voted_at is not None
