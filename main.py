
import uvicorn
import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.routers import items, users
from core.config import settings


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users"
    },
    {
        "name": "items",
        "description": "Operations with items"
    },
    {
        "name": "admin",
        "description": "Admin operations"
    },
    {
        "name": "auth",
        "description": "Authenticate operations"
    }
]

app = FastAPI(
    title=settings.APP_NAME,
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
    openapi_tags=tags_metadata
)


# CORS
cors_origins = [i.strip() for i in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==========


# Sentry log
if not settings.DATABASE_URL: # heroku exceptional
    sentry_sdk.init(
        settings.SENTRY_URL,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    @app.middleware("http")
    async def sentry_exception(request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                user_id = "database_user_id" # when available
                scope.user = {
                    "ip_address": request.client.host,
                    "id": user_id
                }
                sentry_sdk.capture_exception(e)
            raise e
# ==========


# API register
app.include_router(items.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="8000", debug_level="info")
