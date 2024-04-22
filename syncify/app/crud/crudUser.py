from typing import Type, Union, Dict, Any, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from pydantic import EmailStr
from .base import CRUDBase
from ..models.user import User
from ..schemas.user import UserInDb, UserUpdate, UserCreate
from ..core.security import get_password_hash, verify_password


class CrudUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: EmailStr) -> Type[User]:
        try:
            user_by_email = db.query(self.model).filter(self.model.email == email).one()
            if user_by_email is None:
                raise HTTPException(status_code=404, detail='does not exist')
            return user_by_email
        except NoResultFound:
            raise HTTPException(status_code=404, detail='user not found')

    def create(self, db: Session, *, obj_in: UserCreate, admin_mode=False) -> User:
        try:
            db_obj = User(
                email=obj_in.email,
                hashed_password=get_password_hash(obj_in.password),
                full_name=obj_in.full_name
            )
            if admin_mode:
                db_obj.is_superuser = True
                db_obj.is_active = True

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return jsonable_encoder(db_obj)
        except IntegrityError as error:
            db.rollback()
            # logger.warning(f"user exists {error}")
            raise HTTPException(status_code=409, detail='user with this data already exist')
        except SQLAlchemyError as error:
            # logger.error(f'an error occurred creating user: {error}')
            raise HTTPException(status_code=500, detail='An error occurred when creating the user')

    #
    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            return super().update(db, db_obj=db_obj, obj_in=update_data)

        except IntegrityError as error:
            db.rollback()
            raise HTTPException(status_code=409, detail="user with this data already exist")
        except Exception as error:
            raise HTTPException(status_code=500, detail='An error occurred when creating user')

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        try:
            user = self.get_by_email(db, email=email)
            if not user:
                return None
            if not verify_password(password, user.hashed_password):
                return None
            return user
        except Exception as error:
            raise HTTPException(status_code=401, detail="Not Authenticated")

    def is_active(self, user: User) -> bool:
        try:
            return user.is_active
        except Exception:
            # logger.critical(f'operation failed', exc_info=True)
            raise HTTPException(status_code=403, detail="Not Enough Privileges")

    def is_superuser(self, user: User) -> bool:
        try:
            return user.is_superuser
        except Exception as error:
            # logger.error(operation failed \n {error}', exc_info=True)
            raise HTTPException(status_code=403, detail='Not Enough Privileges')


user = CrudUser(User)
