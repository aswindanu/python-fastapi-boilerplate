from sqlalchemy.orm import Session
from models.item import Item
from api.schemas.item import ItemCreate
from crud.base import CRUDBase
from api.schemas.item import ItemSchema, ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    """
    CRUD Item class

    Parameters
    ----------
    model: A SQLAlchemy model class
    schema: A Pydantic model (schema) class

    Methods
    -------
    get_item_by_id(self, db: Session, id: int) -> ItemSchema
        Get item by id
    get_items(self, db: Session, skip: int = 0, limit: int = 100) -> ItemSchema
        Get items list with skip and limit filter query
    get_user_items(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> ItemSchema
        Get user items list with skip and limit filter query
    create_user_item(self, db: Session, item: ItemCreate, user_id: int) -> ItemSchema
        Create new user item
    """

    async def get_item_by_id(self, db: Session, id: int) -> ItemSchema:
        """
        Get item by id

        Parameters
        ----------
        db : Session
            The session database of app
        id : int
            An id that wanted to get

        Returns
        -------
        Object
            An object of ItemSchema
        """
        return super().get(db=db, id=id)

    async def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> ItemSchema:
        """
        Get items list with skip and limit filter query

        Parameters
        ----------
        db : Session
            The session database of app
        skip : int, default=0
            An id that wanted to skip
        limit : int, default=100
            A limit of list data

        Returns
        -------
        Object
            An object of ItemSchema
        """
        return db.query(Item).offset(skip).limit(limit).all()

    async def get_user_items(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> ItemSchema:
        """
        Get user items list with skip and limit filter query

        Parameters
        ----------
        db : Session
            The session database of app
        user_id : int
            An user id that wanted to get
        skip : int, default=0
            An id that wanted to skip
        limit : int, default=100
            A limit of list data

        Returns
        -------
        Object
            An object of ItemSchema
        """
        return db.query(Item).filter(Item.owner_id == user_id).offset(skip).limit(limit).all()

    async def create_user_item(self, db: Session, obj_in: ItemCreate, user_id: int) -> ItemSchema:
        """
        Create new user item

        Parameters
        ----------
        db : Session
            The session database of app
        obj_in : ItemCreate
            A body request object
        user_id : int
            An user id that wanted to get

        Returns
        -------
        Object
            An object of ItemSchema
        """
        db_item = Item(**obj_in.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

crud_item = CRUDItem(Item)
