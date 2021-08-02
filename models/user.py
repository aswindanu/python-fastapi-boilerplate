from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.setup import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(500))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner",
                         cascade="all, delete")
