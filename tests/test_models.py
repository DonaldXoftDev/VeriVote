from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import (
    AnonymousBallot,
    AuditLog,
    BallotChoice,
    BallotQuestion,
    CandidateOption,
    Election,
    ElectionState,
    RuleType,
    User,
    UserRole,
    VoterEligibility,
)


def test_all_eight_3nf_tables_registered() -> None:
    expected_tables = {
        "users",
        "elections",
        "voter_eligibility",
        "ballot_questions",
        "candidate_options",
        "anonymous_ballots",
        "ballot_choices",
        "audit_logs",
    }
    assert expected_tables == set(Base.metadata.tables.keys())


def test_anonymity_air_gap_no_voter_fk_and_no_timestamps() -> None:
    """Verify anonymous_ballots and ballot_choices have zero voter FKs and zero timestamps."""
    ballot_fks = {fk.column.table.name for fk in AnonymousBallot.__table__.foreign_keys}
    choice_fks = {fk.column.table.name for fk in BallotChoice.__table__.foreign_keys}

    assert "voter_eligibility" not in ballot_fks
    assert "voter_eligibility" not in choice_fks
    assert ballot_fks == {"elections"}
    assert choice_fks == {"anonymous_ballots", "ballot_questions", "candidate_options"}

    ballot_cols = set(AnonymousBallot.__table__.columns.keys())
    choice_cols = set(BallotChoice.__table__.columns.keys())
    assert not any("at" in c or "time" in c or "voter" in c for c in ballot_cols)
    assert not any("at" in c or "time" in c or "voter" in c for c in choice_cols)


def test_election_timestamp_driven_lifecycle() -> None:
    now = datetime.now(UTC)
    election = Election(
        title="Lifecycle Test",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=5),
    )
    assert election.get_state(now) == ElectionState.DRAFT
    assert election.is_editable() is True
    assert election.is_open(now) is False

    election.published_at = now
    assert election.get_state(now) == ElectionState.UPCOMING
    assert election.is_editable() is False

    assert election.get_state(now + timedelta(hours=2)) == ElectionState.ACTIVE
    assert election.is_open(now + timedelta(hours=2)) is True

    assert election.get_state(now + timedelta(hours=6)) == ElectionState.CLOSED

    election.cancelled_at = now + timedelta(minutes=30)
    assert election.get_state(now + timedelta(hours=2)) == ElectionState.CANCELLED


def test_ballot_question_validate_choices() -> None:
    q_single = BallotQuestion(
        prompt="President",
        rule_type=RuleType.SINGLE,
        is_required=True,
        min_select=1,
        max_select=1,
    )
    assert q_single.validate_choices([]) is False
    assert q_single.validate_choices([{"option_id": "opt-1"}]) is True
    assert q_single.validate_choices([{"option_id": "opt-1"}, {"option_id": "opt-2"}]) is False

    q_multi = BallotQuestion(
        prompt="Committee",
        rule_type=RuleType.MULTI,
        is_required=False,
        min_select=1,
        max_select=2,
    )
    assert q_multi.validate_choices([]) is True  # optional abstention
    assert q_multi.validate_choices([{"option_id": "o1"}, {"option_id": "o2"}]) is True
    assert q_multi.validate_choices([{"option_id": "o1"}, {"option_id": "o1"}]) is False

    q_ranked = BallotQuestion(
        prompt="Ranked Race",
        rule_type=RuleType.RANKED,
        is_required=True,
        min_select=1,
        max_select=3,
    )
    assert (
        q_ranked.validate_choices(
            [
                {"option_id": "o1", "rank_position": 1},
                {"option_id": "o2", "rank_position": 2},
            ]
        )
        is True
    )
    assert (
        q_ranked.validate_choices(
            [
                {"option_id": "o1", "rank_position": 1},
                {"option_id": "o2", "rank_position": 3},
            ]
        )
        is False
    )


def test_election_end_time_must_exceed_start_time(db_session: Session) -> None:
    user = User(
        email="admin@verivote.edu",
        org_name="NAU Electoral Commission",
        password_hash="hashed-secret",
        role=UserRole.ORGANIZER,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    now = datetime.now(UTC)
    invalid_election = Election(
        organizer_id=user.id,
        title="Invalid Window Election",
        start_time=now,
        end_time=now - timedelta(hours=1),
    )
    db_session.add(invalid_election)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_create_full_8_table_hierarchy(db_session: Session) -> None:
    organizer = User(
        email="chair@verivote.edu",
        org_name="Faculty of Engineering",
        password_hash="hashed-secret",
        role=UserRole.ORGANIZER,
        is_active=True,
    )
    db_session.add(organizer)
    db_session.flush()

    now = datetime.now(UTC)
    election = Election(
        organizer_id=organizer.id,
        title="2026 Faculty President Election",
        description="Annual student executive election",
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(days=1),
        published_at=now - timedelta(hours=2),
    )
    db_session.add(election)
    db_session.flush()

    question = BallotQuestion(
        election_id=election.id,
        prompt="Select Faculty President",
        rule_type=RuleType.SINGLE,
        is_required=True,
        min_select=1,
        max_select=1,
        display_order=1,
    )
    db_session.add(question)
    db_session.flush()

    option_a = CandidateOption(question_id=question.id, label="Candidate A", display_order=1)
    option_b = CandidateOption(question_id=question.id, label="Candidate B", display_order=2)
    db_session.add_all([option_a, option_b])

    voter = VoterEligibility(
        election_id=election.id,
        email="student@nau.edu.ng",
        voter_ref="2024934002",
    )
    db_session.add(voter)
    db_session.flush()
    assert voter.has_voted() is False

    ballot = AnonymousBallot(
        election_id=election.id,
        receipt_hash="sha256-receipt-001",
    )
    db_session.add(ballot)
    db_session.flush()

    choice = BallotChoice(
        ballot_id=ballot.id,
        question_id=question.id,
        option_id=option_a.id,
        rank_position=None,
    )
    db_session.add(choice)
    voter.voted_at = now

    audit = AuditLog(
        user_id=organizer.id,
        action="ELECTION_PUBLISHED",
        target_type="election",
        target_id=election.id,
        details={"title": election.title},
    )
    db_session.add(audit)
    db_session.commit()

    assert voter.has_voted() is True
    assert db_session.query(AnonymousBallot).count() == 1
    assert db_session.query(BallotChoice).count() == 1
    assert db_session.query(AuditLog).count() == 1
