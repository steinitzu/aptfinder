import json

import requests
import pytest

import aptfinder


def test_bedroom_filter():
    url = 'http://localhost:8000/get_apts'
    params = {
        'south': '43.657369233271744',
        'west': '-79.5507067793148',
        'north': '43.695536721863824',
        'east': '-79.49793465976376',
        'radius': '2124.3926974638684',
        'center_lat': '43.676452977567784',
        'center_lng': '-79.52432071953928',
        'coordtype': 'degrees',
        'bedrooms': '2'
        }
    r = requests.get(url, params, stream=True)
    for x in r.json():
        assert x['bedrooms'] >= 2

    params['bedrooms'] = 1
    r = requests.get(url, params, stream=True)
    lowest = 2
    for x in r.json():
        if x['bedrooms'] < lowest:
            lowest = x['bedrooms']
    assert lowest == 1
