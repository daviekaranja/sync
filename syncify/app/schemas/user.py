import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime


class UserUpdate(BaseModel):
    fullname: str
    email: EmailStr


class UserInDb(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    created_at: datetime.datetime
