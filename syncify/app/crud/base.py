from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import exc

from syncify.app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        try:
            item = db.query(self.model).filter(self.model.id == id).one()
            return item
        except exc.NoResultFound:
            raise HTTPException(status_code=404, detail='Not Found')

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    )-> list[tuple[Any]]:
        try:
            items = db.query(self.model).offset(skip).limit(limit).all()
            if items is None:
                raise HTTPException(status_code=404, detail='Not Found!')
            return items
        except exc.NoResultFound as error:
            raise HTTPException(404, detail="Not Found!")

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except exc.IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=409, detail='already exists')

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except exc.IntegrityError as e:
            db.rollback()
            HTTPException(status_code=409, detail='that data already exist')

    def remove(self, db: Session, *, id: int) -> ModelType:
        try:
            obj = db.query(self.model).get(id)
            if obj is None:
                db.rollback()
                raise HTTPException(status_code=404, detail='not found')
            db.delete(obj)
            db.commit()
            return obj
        except exc.IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=409, detail='An Error occured')
        except exc.NoResultFound as e:
            db.rollback()
            raise HTTPException(status_code=404,  detail='Not Found!')
