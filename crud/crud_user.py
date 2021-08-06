from typing import Any, Optional
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


class CRUDUser(CRUDBase[UserSchema, UserCreate, UserUpdate]):
    """
    CRUD User class

    Parameters
    ----------
    model: A SQLAlchemy model class
    schema: A Pydantic model (schema) class

    Methods
    -------
    - User -
    get_user(self, db: Session, user_id: int) -> UserSchema
        Get user by id
    get_user_by_username(self, db: Session, username: int) -> UserSchema
        Get user by username filter query
    get_user_by_email(self, db: Session, email: int) -> UserSchema
        Get user by email filter query
    get_users(self, db: Session, skip: int = 0, limit: int = 100) -> UserSchema
        Get users list with skip and limit filter query
    create_user(self, db: Session, user: UserCreate) -> UserSchema
        Create new user
    update_user(self, db: Session, user:UserSchema, obj_in: UserUpdate) -> UserSchema
        Update existing user

    - Auth -
    is_active(self, user: User) -> bool
        Get user is_active attribute value
    is_superuser(self, user: User) -> bool
        Get user is_superuser attribute value
    verify_password(self, plain_password, hashed_password) -> Any
        Verify inputted plain password with hashed password
    get_password_hash(self, password) -> Any
        Get hashed password from database
    authenticate_user(self, username: str, password: str, db: Session = Depends()) -> Any
        Authenticate user eligible for access
    create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str
        Create access token jwt
    """

    async def get_user(self, db: Session, user_id: int) -> UserSchema:
        """
        Get user by id

        Parameters
        ----------
        db : Session
            The session database of app
        user_id : int
            An id that wanted to get

        Returns
        -------
        Object
            An object of UserSchema
        """
        return await super().get(db=db, id=user_id)

    async def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> UserSchema:
        """
        Get users list with skip and limit filter query

        Parameters
        ----------
        db : Session
            The session database of app
        skip : int, default=0
            A id that wanted to skip
        limit : int, default=100
            A limit of list data

        Returns
        -------
        Object
            An object of UserSchema list
        """
        return await super().get_multi(db=db, skip=skip, limit=limit)

    async def get_user_by_username(self, db: Session, username: str) -> UserSchema:
        """
        Get user by username filter query

        Parameters
        ----------
        db : Session
            The session database of app
        username : str
            A username that wanted to get

        Returns
        -------
        Object
            An object of UserSchema
        """
        return db.query(User).filter(User.username == username).first()

    async def get_user_by_email(self, db: Session, email: str) -> UserSchema:
        """
        Get user by email filter query

        Parameters
        ----------
        db : Session
            The session database of app
        email : str
            An email that wanted to get

        Returns
        -------
        Object
            An object of UserSchema
        """
        return db.query(User).filter(User.email == email).first()

    async def create_user(self, db: Session, obj_in: UserCreate) -> UserSchema:
        """
        Create new user

        Parameters
        ----------
        db : Session
            The session database of app
        obj_in : UserCreate
            A body request object

        Returns
        -------
        Object
            An object of UserSchema
        """
        hashed_password = await self.get_password_hash(obj_in.password)
        db_user = User(
            username=obj_in.username, email=obj_in.email, hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def update_user(self, db: Session, user:UserSchema, obj_in: UserUpdate) -> UserSchema:
        """
        Update existing user

        Parameters
        ----------
        db : Session
            The session database of app
        user : UserSchema
            A user object
        obj_in : UserUpdate
            A body request object

        Returns
        -------
        Object
            An object of UserSchema
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]: ##
            hashed_password = await self.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            user.hashed_password = update_data["hashed_password"]
        return await super().update(db, db_obj=user, obj_in=update_data)


    # ===== AUTH ===== #
    async def is_active(self, user: User) -> bool:
        """
        Get user is_active attribute value

        Parameters
        ----------
        user : User
            A user object

        Returns
        -------
        bool
            is_active attribute value
        """
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        """
        Get user is_superuser attribute value

        Parameters
        ----------
        user : User
            A user object

        Returns
        -------
        bool
            is_superuser attribute value
        """
        return user.is_superuser

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify inputted plain password with hashed password

        Parameters
        ----------
        plain_password : str
            A plain password string from input
        hashed_password : str
            A hashed password string from database

        Returns
        -------
        bool
            True of False
        """
        return pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password) -> Any:
        """
        Get hashed password from database

        Parameters
        ----------
        password : str
            A plain password string from input

        Returns
        -------
        Any
            hashed password from database
        """
        return pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str, db: Session = Depends()) -> Any:
        """
        Authenticate user eligible for access

        Parameters
        ----------
        username : str
            A username string from input
        password : str
            A plain password string from input
        db : Session
            The session database of app

        Returns
        -------
        Any
            True or False, or return a user object
        """
        db_user = await self.get_user_by_username(db, username)
        if not db_user:
            return False
        if not await self.verify_password(password, db_user.hashed_password):
            return False
        return db_user

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create access token jwt

        Parameters
        ----------
        data : dict
            A data that will be encode
        expires_delta : Optional[timedelta], default=None
            An expire jwt parameter

        Returns
        -------
        str
            An encoded token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        enconded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return enconded_jwt

crud_user = CRUDUser(User)