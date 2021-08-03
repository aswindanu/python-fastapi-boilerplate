from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import ReturnTypeFromArgs

from core.config import settings
from models.user import User
from crud.base import CRUDBase
from api.schemas.user import UserSchema, UserCreate, UserUpdate


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    '''
    CRUD User
    '''
    async def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    async def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    async def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    async def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    async def create_user(self, db: Session, user: UserCreate):
        hashed_password = await self.get_password_hash(user.password)
        db_user = User(
            username=user.username, email=user.email, hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def update_user(self, db: Session, user:UserSchema, obj_in: UserUpdate):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = await self.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            user.hashed_password = update_data["hashed_password"]
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    async def delete_user(self, db: Session, user: User):
        db.delete(user)
        db.commit()
        return None

    # ===== AUTH ===== #
    async def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str, db: Session = Depends()):
        db_user = await self.get_user_by_username(db, username)
        if not db_user:
            return False
        if not await self.verify_password(password, db_user.hashed_password):
            return False
        return db_user

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        enconded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return enconded_jwt

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

crud_user = CRUDUser(User)