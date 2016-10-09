from math import radians
from math import degrees as to_degrees

from flask import render_template, request, jsonify

from . import app
from ..locator import to_radians, apartments_in_radius


@app.route('/')
def index():
    return render_template('mapview.html',
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
    apts = []
    for apt in apartments_in_radius(center, radius, bounds):
        apt = dict(apt)

        apt['latitude'] = to_degrees(apt['latitude'])
        apt['longitude'] = to_degrees(apt['longitude'])
        apts.append(apt)
        #apts.append(apt.json(degrees=degrees))
    return jsonify(apts)
