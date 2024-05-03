from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import EmailStr

from syncify.app.api.dependancies import get_db, get_user
from syncify.app.core import security
from syncify.app.core.config import settings
from syncify.app.crud import crudUser
from syncify.app.schemas.user import UserInDb, SessionUser
from syncify.app.scripts.system_logger import logger

router = APIRouter()


@router.post('/login/access-token')
def login_access_token(request: Request, db: Session = Depends(get_db),
                       form_data: OAuth2PasswordRequestForm = Depends()):
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
    user_data = SessionUser(**jsonable_encoder(user))
    request.session['user'] = user_data.dict()
    return access_token


@router.get('/logout', status_code=200)
def logout(request: Request):
    request.session.pop('user')
    return 'logged out'
