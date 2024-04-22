from fastapi import APIRouter

from .endpoints import (
login
)

api_router = APIRouter()
api_router.include_router(login.router, prefix='/auth', tags=['Authentication'])
