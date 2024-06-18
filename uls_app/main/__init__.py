from flask import Blueprint

bp = Blueprint('main',__name__)

from uls_app.main import routes