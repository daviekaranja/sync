import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    # id: int
    fullname: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    fullname: str
    email: EmailStr


class UserInDb(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    created_at: datetime.datetime


class SessionUser(BaseModel):
    id: int
    fullname: str
    is_active: bool
    is_superuser: bool
