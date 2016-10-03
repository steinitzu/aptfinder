from math import radians, sin, cos, asin, sqrt

from .. import db
from ..db.models import Apartment


# Earth radius in km
EARTH_RADIUS = 6371


def to_radians(lat, lng):
    return radians(lat), radians(lng)


def apartments_in_radius(center, radius_meters):
    """
    Get all Apartments falling inside
    circle with given center and radius.
    """
    rkm = radius_meters/1000
    s = db.Session()

    for apt in s.query(Apartment):
        d = haversine((apt.latitude, apt.longitude), center)
        if d <= rkm:
            yield apt


def haversine(pointa, pointb):
    """
    Calculate the great circle distance between two points
    on the earth in kilometers.
    pointa and pointb must be lat and lng coordinates in radians
    """
    print(pointa, pointb)
    lat1, lng1 = pointa
    lat2, lng2 = pointb

    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = EARTH_RADIUS * c
    return km
