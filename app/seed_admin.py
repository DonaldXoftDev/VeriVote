from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models import User
from app.models.enums import UserRole


def seed_admin(db: Session, admin_email: str, admin_password: str) -> User:
    """Create the initial Super-Admin account if it does not already exist."""
    existing = db.execute(select(User).where(User.email == admin_email)).scalar_one_or_none()
    if existing is not None:
        return existing

    admin_record = User(
        email=admin_email,
        password_hash=get_password_hash(admin_password),
        role=UserRole.SUPER_ADMIN,
        is_active=True,
    )
    db.add(admin_record)
    db.commit()
    db.refresh(admin_record)
    return admin_record

if __name__ == "__main__":
    settings = get_settings()
    with SessionLocal() as db:
        try:
            seed_admin(
                db=db,
                admin_email=settings.ADMIN_EMAIL,
                admin_password=settings.ADMIN_PASSWORD,
            )
            print("Admin seeded successfully.")
        except Exception as exc:
            db.rollback()
            raise RuntimeError(f"Admin creation failed: {exc}") from exc
