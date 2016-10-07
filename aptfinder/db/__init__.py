from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import BaseModel
from .. import db_config

engine = create_engine(db_config.DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance


def get_if_exists(session, model, **filterkw):
    item = session.query(model).filter_by(**filterkw).first()
    if item:
        return item
    else:
        return False
