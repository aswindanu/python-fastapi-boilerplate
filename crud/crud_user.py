from sqlalchemy.orm import Session
from models.user import User
from models.item import Item
from api.schemas.user import UserSchema, UserCreate, UserUpdate
from api.auth import auth


async def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


async def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_user(db: Session, user:UserSchema, obj_in: UserUpdate):
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    if update_data["password"]:
        hashed_password = await auth.get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
        user.hashed_password = update_data["hashed_password"]
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


async def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
    return None


# from typing import Any, Dict, Optional, Union

# from sqlalchemy.orm import Session

# from api.auth.auth import get_password_hash, verify_password
# from crud.base import CRUDBase
# from models.user import User
# from api.schemas.user import UserCreate, UserUpdate
# from api.auth import auth


# class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
#     def get_user(self, db: Session, user_id: int):
#         return db.query(User).filter(User.id == user_id).first()


#     def get_user_by_username(self, db: Session, username: str):
#         return db.query(User).filter(User.username == username).first()


#     def get_user_by_email(self, db: Session, email: str):
#         return db.query(User).filter(User.email == email).first()


#     def get_users(self, db: Session, skip: int = 0, limit: int = 100):
#         return db.query(User).offset(skip).limit(limit).all()

#     def create_user(self, db: Session, user: UserCreate):
#         hashed_password = auth.get_password_hash(user.password)
#         db_user = User(
#             username=user.username, email=user.email, hashed_password=hashed_password)
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user


#     def delete_user(self, db: Session, user: User):
#         db.delete(user)
#         db.commit()
#         return None

#     def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
#         return db.query(User).filter(User.email == email).first()

#     def create(
#         self,
#         db: Session,
#         *,
#         obj_in: UserCreate
#     ) -> User:
#         db_obj = User(
#             email=obj_in.email,
#             hashed_password=get_password_hash(obj_in.password),
#             first_name=obj_in.first_name,
#             last_name=obj_in.last_name,
#             address=obj_in.address,
#             mobile_no=obj_in.mobile_no,
#             country_code=obj_in.country_code,
#             is_active=obj_in.is_active,
#             is_superuser=obj_in.is_superuser,
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def update(
#         self,
#         db: Session,
#         *,
#         db_obj: User,
#         obj_in: Union[UserUpdate, Dict[str, Any]]
#     ) -> User:
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.dict(exclude_unset=True)
#         if update_data["password"]:
#             hashed_password = get_password_hash(update_data["password"])
#             del update_data["password"]
#             update_data["hashed_password"] = hashed_password
#         return super().update(db, db_obj=db_obj, obj_in=update_data)

#     def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
#         user = self.get_by_email(db, email=email)
#         if not user:
#             return None
#         if not verify_password(password, user.hashed_password):
#             return None
#         return user

#     def is_active(self, user: User) -> bool:
#         return user.is_active

#     def is_superuser(self, user: User) -> bool:
#         return user.is_superuser


# user = CRUDUser(User)