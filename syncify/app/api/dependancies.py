from typing import Generator
from syncify.app.db.session import SessionLocal
from syncify.app.schemas.user import UserInDb
from fastapi import Request, HTTPException, Depends
from syncify.app.crud.crudUser import user
from sqlalchemy.orm import Session


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(request: Request, db: Session = Depends(get_db)):
    session_user = request.session.get('user')
    if session_user is None:
        raise HTTPException(status_code=401, detail='Not Authenticated')
    userdb = user.get(db, id=session_user['id'])
    return userdb
