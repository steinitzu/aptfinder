"""
This module is responsible for maintaining geocodes on
listings in Database.
"""
from math import radians

import googlemaps

from .. import db
from ..config import GOOGLE_MAPS_API_KEY
from . import celery
from .. import log


def get_rows(num=2500, source='gmaps'):
    c = db.engine.execute(
        'SELECT * FROM apartment WHERE geocode_source != %s',
        source)
    result = c.fetchmany(num)
    c.close()
    return result


def set_geocode(row, latdg, lngdg, source):
    q = '''
        UPDATE apartment
        SET latitude = %s,
        longitude  = %s,
        lat_deg = %s,
        lng_deg = %s,
        geocode_source = %s
        WHERE id = %s;
        '''
    params = (radians(latdg), radians(lngdg), latdg, lngdg, source, row['id'])
    db.engine.execute(q, params)


def delete_row(row):
    db.engine.execute('DELETE FROM apartment WHERE id = %s', row['id'])


def gmaps_geocode_rows(rows):
    for row in rows:
        try:
            loc = gmaps.geocode(apt.address)[0]
        except (IndexError, TypeError) as e:
            # Can't geocode, delete listing
            s.delete(apt)
            continue


def gmap_geocode_rows(rows):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY,
                              timeout=20)
    for i, row in enumerate(rows):
        try:
            # TODO: Set configurable bounds for GTA
            geoc = gmaps.geocode(row['address'], region='CA')
        except (googlemaps.exceptions.Timeout,
                googlemaps.exceptions.TransportError) as e:
            log.error('Geocode failed, original msg: {}'.format(e))
            break
        if not geoc:
            # Listing can't be geocoded, delete
            delete_row(row)
            continue
        loc = geoc[0]
        lat = loc['geometry']['location']['lat']
        lng = loc['geometry']['location']['lng']
        set_geocode(row, lat, lng, 'gmaps')


@celery.task()
def tasked_geocode(num=2000):
    """
    Geocode num apartments from db.
    """
    gmap_geocode_rows(get_rows(num))
