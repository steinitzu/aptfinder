from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import BaseModel
from .. import db_config

engine = create_engine(db_config.DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)
