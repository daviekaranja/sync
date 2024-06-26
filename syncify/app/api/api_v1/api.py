from fastapi import APIRouter
from .endpoints import facebook
from .endpoints import utils

from .endpoints import (
login, users
)

api_router = APIRouter()
api_router.include_router(login.router, prefix='/auth', tags=['Authentication'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(facebook.router, prefix='/facebook', tags=['Facebook'])
api_router.include_router(utils.router, prefix='/utils', tags=['Utilities'])
