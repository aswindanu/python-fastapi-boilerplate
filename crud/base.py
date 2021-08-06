from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Parameters
    ----------
    model: A SQLAlchemy model class
    schema: A Pydantic model (schema) class

    Attributes
    ----------
    model: Type[ModelType]
        model object bound Base

    Methods
    -------
    get(self, db: Session, id: Any) -> Optional[ModelType]
        Get query by id
    get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]
        Get queries list with skip and limit filter query
    create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType
        Create new query
    update(db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType
        Update existing query
    remove(self, db: Session, *, id: int) -> ModelType
        Delete existing query by id
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get query by id

        Parameters
        ----------
        db : Session
            The session database of app
        id : int
            An id that wanted to get

        Returns
        -------
        Object
            An object of ModelType (depend on schema inheritance used)
        """
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get queries list with skip and limit filter query

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
        List[Object]
            An object list of ModelType (depend on schema inheritance used)
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create new query

        Parameters
        ----------
        db : Session
            The session database of app
        * : Any
            Any other object
        obj_in : CreateSchemaType
            A body request object

        Returns
        -------
        Object
            An object of ModelType (depend on schema inheritance used)
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update existing query

        Parameters
        ----------
        db : Session
            The session database of app
        * : Any
            Any other object
        db_obj : ModelType
            A model type object
        obj_in : Union[UpdateSchemaType, Dict[str, Any]]
            A body request object

        Returns
        -------
        Object
            An object of ModelType (depend on schema inheritance used)
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Delete existing query by id

        Parameters
        ----------
        db : Session
            The session database of app
        id : int
            An id that wanted to get

        Returns
        -------
        Object
            An object of ModelType (depend on schema inheritance used)
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
