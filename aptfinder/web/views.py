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
        float(request.args.get('lat')),
        float(request.args.get('lng')))
    radius = float(request.args.get('radius'))
    apts = []
    for apt in apartments_in_radius(center, radius):
        apts.append(apt.json())
    return jsonify(apts)
