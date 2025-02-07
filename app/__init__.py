from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.db import models
from app.config import settings


def create_app() -> FastAPI:
    models.init_db()
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_BACKEND_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routes.register(app)
    return app
