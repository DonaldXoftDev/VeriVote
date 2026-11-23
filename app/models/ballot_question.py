import uuid

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import RuleType


class BallotQuestion(Base):
    """Configurable ballot question with a single voting rule (table: ballot_questions)."""

    __tablename__ = "ballot_questions"

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
    min_select: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_select: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    election: Mapped["Election"] = relationship(  # noqa: F821
        back_populates="questions"
    )
    options: Mapped[list["CandidateOption"]] = relationship(  # noqa: F821
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="CandidateOption.display_order",
    )
