from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from crud import crud_user
from core.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, db: Session = Depends()):
    user = await crud_user.get_user_by_username(db, username)
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    enconded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return enconded_jwt
