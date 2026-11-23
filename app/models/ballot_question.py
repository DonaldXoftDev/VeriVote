import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Text, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import RuleType


class BallotQuestion(Base):
    """Configurable ballot question with a single voting rule (table: ballot_questions)."""

    __tablename__ = "ballot_questions"
    __table_args__ = (
        CheckConstraint("rule_type IN ('SINGLE', 'MULTI', 'RANKED')", name="ck_bq_rule_type"),
        CheckConstraint("min_select >= 1", name="ck_bq_min_select_positive"),
        CheckConstraint("max_select >= min_select", name="ck_bq_max_gte_min"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("elections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    rule_type: Mapped[RuleType] = mapped_column(
        SAEnum(RuleType, name="rule_type", native_enum=False),
        nullable=False,
        default=RuleType.SINGLE,
    )
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    min_select: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_select: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
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

    election: Mapped["Election"] = relationship(  # noqa: F821
        back_populates="questions"
    )
    options: Mapped[list["CandidateOption"]] = relationship(  # noqa: F821
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="CandidateOption.display_order",
    )

    def validate_choices(self, selections: list[dict]) -> bool:
        """Validate a voter's selections for this question against rule_type and bounds."""
        if not selections:
            return not self.is_required

        option_ids = [item.get("option_id") for item in selections]
        if len(set(option_ids)) != len(option_ids):
            return False

        if self.rule_type == RuleType.SINGLE:
            return len(selections) == 1 and all(
                item.get("rank_position") is None for item in selections
            )

        if self.rule_type == RuleType.MULTI:
            return (
                self.min_select <= len(selections) <= self.max_select
                and all(item.get("rank_position") is None for item in selections)
            )

        if self.rule_type == RuleType.RANKED:
            ranks = [item.get("rank_position") for item in selections]
            if any(not isinstance(r, int) or r < 1 for r in ranks):
                return False
            return sorted(ranks) == list(range(1, len(selections) + 1))

        return False
