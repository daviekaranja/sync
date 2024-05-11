from fastapi import APIRouter, Request, HTTPException

from syncify.app.core.config import settings
from syncify.app.intergrations.facebook import oauth

router = APIRouter()


@router.get('/login', status_code=200)
async def login_with_facebook(request: Request):
    state = settings.google_state
    request.session['state'] = state
    redirect_uri = request.url_for('facebook_redirect')
    return await oauth.facebook.authorize_redirect(request, redirect_uri, state=request.session['state'])


@router.get('/auth-redirect', status_code=200)
async def facebook_redirect(request: Request, state: str = None, code: str = None):
    token = await oauth.facebook.authorize_access_token(request)
    if token:
        userdata = token.get('userinfo')
    return userdata
