from typing import List

from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.orm import Session

from syncify.app.models.user import User
from syncify.app.schemas.user import UserCreate, UserUpdate, UserInDb, SessionUser
from syncify.app.crud import crudUser
from syncify.app.api import dependancies

router = APIRouter()


@router.get('/get-me', status_code=200, response_model=UserInDb)
def get_current_user(current_user=Depends(dependancies.get_user)):
    return current_user


@router.get('/get-users', status_code=200, response_model=List[UserInDb])
def get_users(db: Session = Depends(dependancies.get_db), current_user: User  = Depends(dependancies.get_user)) -> List[UserInDb]:
    if current_user.is_superuser:
        user = crudUser.user.get_multi(db)
    else:
        raise HTTPException(status_code=403, detail='Not enough privileges')
    if user is None:
        raise HTTPException(status_code=404, detail='Not Found')
    return user


@router.get('/get-user-by-id/{userId}', status_code=200, response_model=UserInDb)
def get_by_id(db: Session = Depends(dependancies.get_db), *, userId: int):
    user = crudUser.user.get(db, userId)
    if user is None:
        raise HTTPException(status_code=404, detail='Not found')
    return user


@router.post('/create-user', response_model=UserInDb, status_code=201)
def new_user(userdata: UserCreate, db: Session = Depends(dependancies.get_db)):
    new_user = crudUser.user.create(db, obj_in=userdata)
    return new_user


@router.put('/update-user/{userId}', status_code=201, response_model=UserInDb)
def update_user(db: Session = Depends(dependancies.get_db), *, obj_in: UserUpdate, userId: int):
    db_obj: User = crudUser.user.get(db, userId)
    new_user = crudUser.user.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return new_user


@router.delete('/remove-user', status_code=204)
def delete_user(db: Session = Depends(dependancies.get_db), *, userId: int):
    user = crudUser.user.remove(db=db, id=userId)
