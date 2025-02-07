from fastapi import APIRouter, FastAPI

from app import utils


def register(app: FastAPI):
    for module in utils.import_submodules(__name__):
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            app.include_router(router, prefix="/api")