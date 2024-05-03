from fastapi import APIRouter

from .endpoints import (
login, users
)

api_router = APIRouter()
api_router.include_router(login.router, prefix='/auth', tags=['Authentication'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
