from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Numeric, Boolean

BaseModel = declarative_base()


class Apartment(BaseModel):
    __tablename__ == 'apartment'

    id = Column(Integer, primary_key=True)
    date_listed = Column(DateTime)
    url = Column(String)
    address = Column(String)
    price = Column(Numeric)
    price_currency = Column(String, default='CAD')
    pet_friendly = Column(Boolean)
    bathrooms = Column(Integer)
    furnished = Column(Boolean)
