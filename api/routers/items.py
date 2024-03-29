from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from api.schemas.item import ItemSchema, ItemCreate
from api.schemas.user import UserSchema
from api.deps import get_db, get_current_user
from crud.crud_item import crud_item


router = APIRouter()


@router.get("/items", response_model=List[ItemSchema], tags=['admin'])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    GET Get items list
    """
    items = await crud_item.get_items(db=db, skip=skip, limit=limit)
    return items


@router.get("/users/me/items", response_model=List[ItemSchema], tags=['items'])
async def read_user_items(
    skip: int = 0,
    limit: int = 0,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET Get user me items list
    """
    items = await crud_item.get_user_items(db=db, user_id=current_user.id)
    return items


@router.post("/users/{user_id}/items", response_model=ItemSchema, tags=['items'])
async def create_item_for_user(
    item: ItemCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    GET Get user list by user id
    """
    return await crud_item.create_user_item(db=db, obj_in=item, user_id=user_id)
