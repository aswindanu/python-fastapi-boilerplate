from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext

from database.base import *
from database.setup import SessionLocal


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Database initial data
INITIAL_DATA = {
      'User': [
            {
                  'username': 'superuser',
                  'email': 'superuser@example.com',
                  'hashed_password': pwd_context.hash('123')
            },
            {
                  'username': 'admin',
                  'email': 'admin@example.com',
                  'hashed_password': pwd_context.hash('123')
            }
      ],
    #   'sometable': [
    #         {'column1': 'value', 'column2': 'value'}
    #   ]
}

with SessionLocal() as session:
    for data in INITIAL_DATA["User"]:
        session.add(User(**data))
        session.commit()
        session.flush()