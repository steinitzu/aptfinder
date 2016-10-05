from math import radians, sin, cos, asin, sqrt

from .. import db
from ..db.models import Apartment


# Earth radius in km
EARTH_RADIUS = 6371


def to_radians(lat, lng):
    return radians(lat), radians(lng)


def apartments_in_radius(center, radius_meters, bounds):
    """
    Get all Apartments falling inside
    circle with given center and radius.
    """
    rkm = radius_meters/1000
    s = db.Session()

    q = s.query(Apartment)
    bn, bs, be, bw = (bounds['north'], bounds['south'],
                      bounds['east'], bounds['west'])

    # Start by selecting all listings that fall within
    # the circle's bounds (treat it like a rectangle)
    filterq = q.filter(Apartment.latitude != None,
                       Apartment.latitude <= bn,
                       Apartment.latitude >= bs,
                       Apartment.longitude <= be,
                       Apartment.longitude >= bw)

    # Next, check haversine distance for found listings
    # for a more precise result
    for apt in filterq:
        d = haversine((apt.latitude, apt.longitude), center)
        if d <= rkm:
            yield apt


def haversine(pointa, pointb):
    """
    Calculate the great circle distance between two points
    on the earth in kilometers.
    pointa and pointb must be lat and lng coordinates in radians
    """
    lat1, lng1 = pointa
    lat2, lng2 = pointb

    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = EARTH_RADIUS * c
    return km
