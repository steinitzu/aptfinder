from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import (Column, String, Integer,
                        DateTime, Numeric, Boolean,
                        Float)

BaseModel = declarative_base()


class Apartment(BaseModel):
    __tablename__ = 'apartment'

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime,
                        server_default=func.current_timestamp())
    touched_at = Column(DateTime,
                        server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())
    date_listed = Column(DateTime)
    url = Column(String, unique=True, nullable=False)
    address = Column(String)
    price = Column(Numeric)
    price_currency = Column(String, default='CAD')
    pet_friendly = Column(Boolean)
    bathrooms = Column(Integer)
    furnished = Column(Boolean)
    latitude = Column(Float)
    longitude = Column(Float)

    def json(self):
        j = {}
        for key in self._sa_class_manager.keys():
            j[key] = getattr(self, key)
        return j
