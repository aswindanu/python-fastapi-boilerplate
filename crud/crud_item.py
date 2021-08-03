from sqlalchemy.orm import Session
from models.item import Item
from api.schemas.item import ItemCreate
from crud.base import CRUDBase
from api.schemas.item import ItemSchema, ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    '''
    CRUD Item
    '''
    async def get_item_by_id(self, db: Session, id: int):
        return db.query(Item).filter(Item.id == id).first()

    async def get_items(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Item).offset(skip).limit(limit).all()

    async def get_user_items(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Item).filter(Item.owner_id == user_id).offset(skip).limit(limit).all()

    async def create_user_item(self, db: Session, item: ItemCreate, user_id: int):
        db_item = Item(**item.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

crud_item = CRUDItem(Item)
