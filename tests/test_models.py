from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import (
    AnonymousVote,
    AuthMode,
    BallotQuestion,
    CandidateOption,
    Election,
    ElectionOrganizer,
    ElectionStatus,
    RuleType,
    VoterEligibility,
)


def test_all_six_core_tables_registered() -> None:
    expected_tables = {
        "organizers",
        "elections",
        "voter_eligibility",
        "ballot_questions",
        "candidate_options",
        "anonymous_votes",
    }
    assert expected_tables.issubset(set(Base.metadata.tables.keys()))


def test_anonymity_air_gap_no_voter_fk() -> None:
    """Verify anonymous_votes has zero foreign keys pointing to voter_eligibility."""
    referenced_tables = {fk.column.table.name for fk in AnonymousVote.__table__.foreign_keys}
    assert "voter_eligibility" not in referenced_tables
    assert referenced_tables == {"elections", "ballot_questions", "candidate_options"}


def test_election_end_time_must_exceed_start_time(db_session: Session) -> None:
    organizer = ElectionOrganizer(
        email="admin@verivote.edu",
        org_name="NAU Electoral Commission",
        password_hash="hashed-secret",
    )
    db_session.add(organizer)
    db_session.flush()

    now = datetime.now(UTC)
    invalid_election = Election(
        organizer_id=organizer.id,
        title="Invalid Window Election",
        auth_mode=AuthMode.CSV_ROSTER,
        status=ElectionStatus.DRAFT,
        start_time=now,
        end_time=now - timedelta(hours=1),
    )
    db_session.add(invalid_election)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_create_full_election_hierarchy_and_decoupled_vote(db_session: Session) -> None:
    organizer = ElectionOrganizer(
        email="chair@verivote.edu",
        org_name="Faculty of Engineering",
        password_hash="hashed-secret",
    )
    db_session.add(organizer)
    db_session.flush()

    now = datetime.now(UTC)
    election = Election(
        organizer_id=organizer.id,
        title="2026 Faculty President Election",
        auth_mode=AuthMode.CSV_ROSTER,
        status=ElectionStatus.ACTIVE,
        start_time=now,
        end_time=now + timedelta(days=1),
    )
    db_session.add(election)
    db_session.flush()

    question = BallotQuestion(
        election_id=election.id,
        prompt="Select Faculty President",
        rule_type=RuleType.SINGLE,
        min_select=1,
        max_select=1,
    )
    db_session.add(question)
    db_session.flush()

    option_a = CandidateOption(question_id=question.id, label="Candidate A", display_order=1)
    option_b = CandidateOption(question_id=question.id, label="Candidate B", display_order=2)
    db_session.add_all([option_a, option_b])

    voter = VoterEligibility(
        election_id=election.id,
        identifier_hash="sha256-voter-id",
        otp_token_hash="sha256-otp-token",
        has_voted=False,
    )
    db_session.add(voter)
    db_session.flush()

    vote = AnonymousVote(
        election_id=election.id,
        question_id=question.id,
        option_id=option_a.id,
        rank_position=None,
        receipt_hash="sha256-receipt-001",
    )
    voter.has_voted = True
    voter.voted_at = now
    db_session.add(vote)
    db_session.commit()

    assert db_session.query(AnonymousVote).count() == 1
    assert db_session.query(VoterEligibility).filter_by(has_voted=True).count() == 1
