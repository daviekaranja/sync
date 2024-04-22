from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Query, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from syncify.app.api.dependancies import get_db
from syncify.app.core import security
from syncify.app.crud import crudUser
from syncify.app.core.config import settings

router = APIRouter()


@router.post('/login/access-token')
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crudUser.user.authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=401, detail='incorrect email or password')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

    return access_token
