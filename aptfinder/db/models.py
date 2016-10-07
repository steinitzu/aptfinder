from math import degrees as to_degrees

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
    title = Column(String)
    address = Column(String)
    price = Column(Numeric)
    price_currency = Column(String, default='CAD')
    pet_friendly = Column(Boolean)
    bedrooms = Column(String)
    bathrooms = Column(Integer)
    furnished = Column(Boolean)
    latitude = Column(Float)
    longitude = Column(Float)
    geocode_source = Column(String)

    def json(self, degrees=False):
        j = {}
        for key in self._sa_class_manager.keys():
            val = getattr(self, key)
            if key in ('latitude', 'longitude') and degrees:
                val = to_degrees(val)
            j[key] = val
        return j
