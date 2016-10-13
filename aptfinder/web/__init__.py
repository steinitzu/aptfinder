from flask import Flask
from flask_compress import Compress

from .. import db

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from . import views

Compress(app)


@app.before_first_request
def initialize_database():
    db.init_db()
