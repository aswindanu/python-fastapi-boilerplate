from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from api.deps import get_db
from database.base import Base
from core.config import settings


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
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
