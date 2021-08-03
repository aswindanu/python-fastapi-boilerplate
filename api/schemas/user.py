from typing import List, Optional
from pydantic import BaseModel, EmailStr
from api.schemas.item import ItemSchema


class UserBase(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


class UserUpdate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool
    items: List[ItemSchema] = []

    class Config:
        orm_mode = True
