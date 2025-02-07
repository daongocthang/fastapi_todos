from app.db import Base, engine

from app import utils


def init_db():
    utils.import_submodules(__name__)
    Base.metadata.create_all(bind=engine)
