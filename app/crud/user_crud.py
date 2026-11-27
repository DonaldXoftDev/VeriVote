import uuid

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import UserCreate


class UserCRUD(CRUDBase[User, UserCreate, BaseModel]):
    """CRUD operations for the `users` table (flush-only; no commits)."""

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """Fetch a user by email address (case-normalized)."""
        raise NotImplementedError("Scheduled for Sprint 1A implementation")

    def list_organizers(
        self,
        db: Session,
        *,
        is_active: bool | None = None,
    ) -> list[User]:
        """List organizer accounts, optionally filtered by activation status."""
        raise NotImplementedError("Scheduled for Sprint 1A implementation")

    def set_active_status(
        self,
        db: Session,
        *,
        user: User,
        is_active: bool,
    ) -> User:
        """Update `user.is_active` and flush changes to the session."""
        raise NotImplementedError("Scheduled for Sprint 1A implementation")

    def get_organizer_by_id(self, db: Session, *, user_id: uuid.UUID) -> User | None:
        """Fetch an organizer record by UUID."""
        raise NotImplementedError("Scheduled for Sprint 1A implementation")


user_crud = UserCRUD(User)
