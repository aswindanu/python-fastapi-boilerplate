from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database.base import *
from database.setup import engine, settings


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

def get_url():
    connection = settings.DATABASE
    user = settings.DATABASE_USER
    password = settings.DATABASE_PASSWORD
    name = settings.DATABASE_NAME
    host = settings.DATABASE_HOST
    port = settings.DATABASE_PORT
    return f"{connection}://{user}:{password}@{host}:{port}/{name}"


SQLALCHEMY_DATABASE_URL = get_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)

with Session(engine) as session:
    for data in INITIAL_DATA["User"]:
        session.add(User(**data))
        session.commit()
        # session.flush()