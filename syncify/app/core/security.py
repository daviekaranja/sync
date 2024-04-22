import base64
from datetime import timedelta
from typing import Union, Any

import bcrypt
from jose import jwt
from jose.exceptions import JWTError
from syncify.app.core.config import settings


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = settings.get_local_time_with_timezone() + expires_delta
    else:
        expire = settings.get_local_time_with_timezone() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_HOURS
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_to_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(pwd_to_bytes, base64.b64decode(hashed_password.encode('utf-8')))


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    return base64.b64encode(bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())).decode('utf-8')
