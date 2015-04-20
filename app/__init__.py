from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy

# Inits app
app = Flask(__name__)
app.config.from_object('config')

# Inits database
db = SQLAlchemy(app)

from app.views import main_views, book_views, order_views
from app.models import books, orders
