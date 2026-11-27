from typing import Any

from pydantic import BaseModel

from app.db.base import Base
from app.db.session import Session


class CRUDBase[
    ModelType: Base,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]:
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchemaType, **extrafields: Any) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(), **extrafields)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj
