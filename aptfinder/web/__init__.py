from flask import Flask

from .. import db

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from . import views


@app.before_first_request
def initialize_database():
    db.init_db()
