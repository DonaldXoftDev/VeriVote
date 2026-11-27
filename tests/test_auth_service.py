import pytest
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserCreate, UserLogin


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_register_organizer_creates_inactive_user_and_audit_log(db_session: Session) -> None:
    """Should create ORGANIZER with is_active=False, hashed password, and AuditLog entry."""
    _ = (db_session, UserCreate)


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_register_organizer_duplicate_email_raises_conflict(db_session: Session) -> None:
    """Should raise ConflictError when registering an already-existing email."""
    _ = db_session


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_login_returns_bearer_token_for_active_user(db_session: Session) -> None:
    """Should return TokenResponse with valid JWT when credentials match an active user."""
    _ = (db_session, UserLogin)


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_login_rejects_wrong_password_with_unauthorized(db_session: Session) -> None:
    """Should raise UnauthorizedError on wrong password or unknown email."""
    _ = db_session


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_login_rejects_inactive_organizer_with_forbidden(db_session: Session) -> None:
    """Should raise ForbiddenError when an unapproved or suspended organizer logs in."""
    _ = db_session


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_activate_and_suspend_organizer_updates_status_and_logs(db_session: Session) -> None:
    """Should toggle is_active and append AuditLog entries; raise NotFoundError if missing."""
    _ = (db_session, User)
