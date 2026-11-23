import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VoterEligibility(Base):
    """Accreditation roll isolated from anonymous ballots (table: voter_eligibility).

    SECURITY INVARIANT: Never add a foreign key or direct link between this table
    and `anonymous_votes`.
    """

    __tablename__ = "voter_eligibility"
    __table_args__ = (
        UniqueConstraint("election_id", "identifier_hash", name="uq_voter_election_identifier"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("elections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    identifier_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    otp_token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    has_voted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    voted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    election: Mapped["Election"] = relationship(  # noqa: F821
        back_populates="eligible_voters"
    )
