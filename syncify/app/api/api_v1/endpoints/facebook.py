from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from syncify.app.scripts.system_logger import logger

from syncify.app.core.config import settings
from syncify.app.intergrations.facebook import oauth, OAuthError

router = APIRouter()


@router.get('/login', status_code=200)
async def login_with_facebook(request: Request):
    state = settings.google_state
    request.session['state'] = state
    redirect_uri = request.url_for('facebook_redirect')
    logger.info(redirect_uri)
    return await oauth.facebook.authorize_redirect(request, redirect_uri, state=request.session['state'])


@router.get('/auth-redirect', status_code=200)
async def facebook_redirect(request: Request, state: str = None, code: str = None):
    try:
        token = await oauth.facebook.authorize_access_token(request)
        userdata = token.get('userinfo')
        logger.info(userdata)
        return userdata
    except OAuthError as e:
        logger.info(e.error)
        html_error = f"<h1>{e.error}</h1>"
        return HTMLResponse(html_error)

