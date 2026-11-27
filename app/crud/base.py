from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base


class CRUDBase[
    ModelType: Base,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]:
    """Generic CRUD base with flush-only persistence (services own db.commit())."""

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        """Fetch a single record by primary key."""
        return db.execute(select(self.model).where(self.model.id == id)).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: CreateSchemaType, **extrafields: Any) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(), **extrafields)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj
