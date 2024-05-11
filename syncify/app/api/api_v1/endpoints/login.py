from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import secrets
from starlette.requests import Request as Req

from syncify.app.api.dependancies import get_db
from syncify.app.intergrations.google import oauth, OAuthError
from syncify.app.core import security
from syncify.app.core.config import settings
from syncify.app.crud import crudUser
from syncify.app.schemas.user import SessionUser, UserCreate
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
    request.session.get('user')
    return 'logged out'


@router.get('/login/google', status_code=200)
async def google_login(request: Req):
    try:
        state = settings.google_state
        request.session['state'] = state
        redirect_uri = request.url_for('callback')
        return await oauth.google.authorize_redirect(request, redirect_uri, state=request.session['state'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


@router.get('/google/callback', status_code=200)
async def callback(request: Req, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        userdata = token.get('userinfo')
    except OAuthError as e:
        raise HTTPException(status_code=401, detail=e.error)
    if userdata['email_verified']:
        new_user = UserCreate(
            email=userdata['email'],
            password='safaricom',
            fullname=userdata['name']
        )
        create_user = crudUser.user.create(db, obj_in=new_user)
        user_data = SessionUser(**jsonable_encoder(create_user))
        request.session['user'] = user_data.dict()
    return RedirectResponse('/')

