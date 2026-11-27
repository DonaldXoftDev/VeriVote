from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password_hash
from app.models import User
from app.models.enums import UserRole
from app.seed_admin import seed_admin


def test_seed_admin_creates_active_super_admin_with_null_org_name(db_session: Session) -> None:
    admin = seed_admin(
        db=db_session,
        admin_email="superadmin@verivote.edu",
        admin_password="StrongPassword123!",
    )

    assert admin.email == "superadmin@verivote.edu"
    assert admin.org_name is None
    assert admin.role == UserRole.SUPER_ADMIN
    assert admin.is_active is True
    assert verify_password_hash("StrongPassword123!", admin.password_hash) is True


def test_seed_admin_is_idempotent(db_session: Session) -> None:
    first = seed_admin(
        db=db_session,
        admin_email="superadmin@verivote.edu",
        admin_password="StrongPassword123!",
    )
    second = seed_admin(
        db=db_session,
        admin_email="superadmin@verivote.edu",
        admin_password="DifferentPassword999!",
    )

    assert first.id == second.id
    all_admins = db_session.execute(select(User)).scalars().all()
    assert len(all_admins) == 1
