"""
This module is responsible for maintaining geocodes on
listings in Database.
"""
from math import radians

from sqlalchemy import or_
import googlemaps

from ..db import Session
from ..db.models import Apartment
from ..config import GOOGLE_MAPS_API_KEY
from . import celery


def get_rows(num=2500):
    """
    Get rows with missing geocodes from database.
    """
    s = Session()
    result = s.query(Apartment).filter(or_(
        Apartment.latitude==None,
        Apartment.longitude==None))
    ret = []
    for i, a in enumerate(result):
        if i+1 > num:  # i starts at 0
            break
        ret.append(a)
    s.close()
    return ret


def geocode(apartments):
    s = Session()
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    for i, apt in enumerate(apartments):
        try:
            loc = gmaps.geocode(apt.address)[0]
        except (IndexError, TypeError) as e:
            # Can't geocode, delete listing
            s.delete(apt)
            continue
        lat = radians(loc['geometry']['location']['lat'])
        lng = radians(loc['geometry']['location']['lng'])
        apt.latitude = lat
        apt.longitude = lng
        s.add(apt)
        if i % 100 == 0:
            s.flush()
    s.commit()


@celery.task()
def tasked_geocode(num=2000):
    """
    Geocode num apartments from db.
    """
    geocode(get_rows(num))
