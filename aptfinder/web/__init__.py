from flask import Flask

from .. import db

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from . import views
