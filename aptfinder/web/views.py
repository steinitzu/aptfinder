from math import radians
from math import degrees as to_degrees

from flask import render_template, request, json, Response

from . import app
from ..locator import to_radians, apartments_in_radius
from .. import db


@app.route('/')
def index():
    return render_template('reactmap.html',
                           gmaps_key=app.config['GOOGLE_MAPS_API_KEY'])


@app.route('/get_apts', methods=['GET'])
def apartments_in_circle():
    center = to_radians(
        float(request.args.get('center_lat')),
        float(request.args.get('center_lng')))
    radius = float(request.args.get('radius'))
    bounds = {key: radians(float(request.args[key]))
              for key in ('north', 'south', 'east', 'west')}
    degrees = request.args.get('coordtype', 'radians') == 'degrees'

    def aptgen():
        for apt in apartments_in_radius(center, radius, bounds):
            apt = dict(apt)
            if degrees:
                apt['latitude'] = to_degrees(apt['latitude'])
                apt['longitude'] = to_degrees(apt['longitude'])
                yield apt

    return Response(generate(aptgen()), content_type='application/json')


@app.route('/random_apts', methods=['GET'])
def random_apts():
    num = int(request.args.get('num'))
    c = db.engine.execute('SELECT * FROM apartment')
    res = c.fetchmany(num)
    c.close()

    def aptgen():
        for apt in res:
            apt = dict(apt)
            apt['latitude'] = to_degrees(apt['latitude'])
            apt['longitude'] = to_degrees(apt['longitude'])
            yield apt
    return Response(generate(aptgen()), content_type='application/json')


def generate(items):
    """
    A lagging generator to stream JSON
    so we don't have to hold everything in memory
    This is a little tricky,
    as we need to omit the last comma to make valid JSON,
    thus we use a lagging generator,
    similar to http://stackoverflow.com/questions/1630320/
    """
    try:
        prev_item = next(items)  # get first result
    except StopIteration:
        # StopIteration here means the length was zero,
        # so yield a valid items doc and stop
        yield '[]'
        raise StopIteration
    # We have some items. First, yield the opening json
    yield '['
    # Iterate over the items
    for item in items:
        yield json.dumps(prev_item) + ', '
        prev_item = item
    # Now yield the last iteration without comma but with the closing brackets
    yield json.dumps(prev_item) + ']'


def pipe_generate(items):
    try:
        prev_item = next(items)  # get first result
    except StopIteration:
        # StopIteration here means the length was zero,
        # so yield a valid items doc and stop
        yield ''
        raise StopIteration
    # Iterate over the items
    for item in items:
        yield json.dumps(prev_item) + '\n\n'
        prev_item = item
