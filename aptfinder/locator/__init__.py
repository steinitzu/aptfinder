from math import radians, sin, cos, asin, sqrt

from .. import db

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
    rrad = rkm/EARTH_RADIUS

    bn, bs, be, bw = (bounds['north'], bounds['south'],
                      bounds['east'], bounds['west'])

    res = db.engine.execute(
        '''
        SELECT * FROM apartment WHERE
        price is not %s AND
        (latitude <= %s AND
        latitude >= %s AND
        longitude <= %s AND
        longitude >= %s) AND
        acos(sin(%s) * sin(latitude) + cos(%s) * cos(latitude) * cos(longitude - (%s))) <= %s;
        ''',
        (None, bn, bs, be, bw,
         center[0], center[0], center[1], rrad))
    for apt in res:
        yield apt
    res.close()
    return

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
