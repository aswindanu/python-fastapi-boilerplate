from typing import Any, List
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from crud.crud_user import crud_user
from core.config import settings
from services.messaging.email import send_email
from api.deps import get_db, oauth2_scheme, get_current_user
from api.schemas.user import UserSchema, UserCreate, UserUpdate
from database.base import User
from api import dresp


router = APIRouter()


@router.post("/token", tags=['auth'])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    POST Create token jwt
    """
    db_user = await crud_user.authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await crud_user.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/users",
    response_model=List[UserSchema],
    tags=['admin'],
    dependencies=[Depends(get_current_user)])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> UserSchema:
    """
    GET Get users list
    """
    db_users = await crud_user.get_users(db=db, skip=skip, limit=limit)
    return db_users


@router.get(
    "/users/me",
    response_model=UserSchema,
    tags=['users'])
async def read_users_me(
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserSchema:
    """
    GET Get current user
    """
    return current_user


@router.get(
    "/users/{user_id}",
    response_model=UserSchema,
    tags=['admin'],
    dependencies=[Depends(get_current_user)])
async def read_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserSchema:
    """
    GET Get user by id
    """
    db_user = await crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=dresp.NOT_FOUND)
    return db_user


@router.post(
    "/users",
    response_model=UserSchema,
    tags=['users'])
async def create_user(
    obj_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> UserSchema:
    """
    POST Create user
    """
    db_user = await crud_user.get_user_by_email(db=db, email=obj_in.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    if settings.SMTP_SERVER != "your_stmp_server_here":
        background_tasks.add_task(send_email, obj_in.email,
                                  message=f"You've created your account!")
    try:
        return await crud_user.create_user(db=db, obj_in=obj_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")


@router.put(
    "/users",
    response_model=UserSchema,
    tags=['users']
)
async def update_user(
    obj_in: UserUpdate,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserSchema:
    """
    PUT Update user
    """
    return await crud_user.update_user(db=db, user=current_user, obj_in=obj_in)


@router.delete(
    "/users/{user_id}",
    tags=['admin']
)
async def remove_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    DELETE Delete user
    """
    db_user = await crud_user.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=dresp.NOT_FOUND)
    await crud_user.remove(db=db, id=id)
    return {"detail": f"User with id {db_user.id} successfully deleted"}
