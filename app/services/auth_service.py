import uuid

from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import LogoutUser, TokenResponse, UserCreate, UserLogin


class AuthService:
    """Authentication & Governance Module (Sprint 1A).

    Orchestrates organizer registration (`is_active=False`), login, logout,
    Super-Admin organizer activation/suspension, and immutable `audit_logs`
    entries. Services own transaction boundaries (`db.commit()` / `db.rollback()`).
    """

    @staticmethod
    def register_organizer(db: Session, payload: UserCreate) -> User:
        """Register a new inactive organizer account.

        Steps:
        1. Check `user_crud.get_by_email` — raise `ConflictError` if email exists.
        2. Hash `payload.password` via `get_password_hash`.
        3. Persist `User` with `role=UserRole.ORGANIZER`, `is_active=False`.
        4. Record `ORGANIZER_REGISTERED` in `audit_crud.create_log`.
        5. `db.commit()` and return the created `User`.
        """
        raise NotImplementedError("Scheduled for Sprint 1A")

    @staticmethod
    def login(db: Session, payload: UserLogin) -> TokenResponse:
        """Authenticate a user and issue a Bearer JWT.

        Steps:
        1. Lookup user by email — raise `UnauthorizedError` on missing user or bad password.
        2. Verify `user.is_active` — raise `ForbiddenError` if pending/suspended.
        3. Create JWT via `create_access_token` and return `TokenResponse`.
        """
        raise NotImplementedError("Scheduled for Sprint 1A")

    @staticmethod
    def logout(current_user: User) -> LogoutUser:
        """Return stateless logout confirmation for the authenticated user."""
        raise NotImplementedError("Scheduled for Sprint 1A")

    @staticmethod
    def list_organizers(db: Session, *, is_active: bool | None = None) -> list[User]:
        """List organizer accounts for Super-Admin review."""
        raise NotImplementedError("Scheduled for Sprint 1A")

    @staticmethod
    def activate_organizer(db: Session, *, admin: User, organizer_id: uuid.UUID) -> User:
        """Activate a pending/suspended organizer and record an audit log.

        Raises `NotFoundError` if the organizer does not exist.
        """
        raise NotImplementedError("Scheduled for Sprint 1A")

    @staticmethod
    def suspend_organizer(db: Session, *, admin: User, organizer_id: uuid.UUID) -> User:
        """Suspend an organizer account and record an audit log.

        Raises `NotFoundError` if the organizer does not exist.
        """
        raise NotImplementedError("Scheduled for Sprint 1A")
