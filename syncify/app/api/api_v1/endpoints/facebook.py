from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.get('/login', status_code=200)
async def login_with_facebook(request: Request):
    pass


@router.get('/auth-redirect', status_code=200)
async def facebook_redirect(request: Request):
    return "facebook"
