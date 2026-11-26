from sqlalchemy.orm import Session


class AuthService:
    """Authentication & Governance Module (Sprint 1).

    Handles organizer registration (is_active=False), Super-Admin activation,
    password hashing (Bcrypt/Argon2), login, and immutable audit_logs entries.
    """

    @staticmethod
    def register_organizer(db: Session, email: str, org_name: str, password: str) -> None:

        #verify the user isn't already registered,
        #hash the password
        #set the user as organizer and add to the db
        #return the record schema
        raise NotImplementedError("Scheduled for Sprint 1")

    @staticmethod
    def activate_organizer(db: Session, admin_id: str, organizer_id: str) -> None:
        raise NotImplementedError("Scheduled for Sprint 1")

    @staticmethod
    def login(email: str, password: str):
        pass

    @staticmethod
    def logout():
        pass

