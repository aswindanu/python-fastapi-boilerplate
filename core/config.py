import os
from dotenv import load_dotenv
from pydantic import BaseSettings

cwd = os.getcwd()
env_file = "/".join(cwd.split("/")[:-1]) + ".env"
print(env_file)
load_dotenv(dotenv_path=env_file)

class Settings(BaseSettings):
    # config
    APP_NAME: str = "FastAPI Boilerplate"
    EMAIL_SENDER: str = "no-reply@app.com"
    SMTP_SERVER: str = "your_stmp_server_here"

    API_V1_STR = ""
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    DEV: int = os.environ.get("DEV", 0)

    DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "127.0.0.1")
    DATABASE_PORT: int = os.environ.get("DATABASE_PORT", 5432)
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "Hobby-dev")
    DATABASE_USER: str = os.environ.get("DATABASE_USER", "postgres")
    DATABASE_PASS: str = os.environ.get("DATABASE_PASS", "")

    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")  # only for heroku

    CORS_ORIGINS: str = os.environ.get("CORS_ORIGINS", "")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    SENTRY_URL: str = os.environ.get("SENTRY_URL", "")

settings = Settings()
