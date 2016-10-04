from flask import render_template

from . import app


@app.route('/')
def index():
    return render_template('mapview.html',
                           gmaps_key=app.config['GOOGLE_MAPS_API_KEY'])
