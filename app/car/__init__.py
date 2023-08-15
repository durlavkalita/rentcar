from flask import Blueprint

bp = Blueprint("car", __name__)

from app.car import routes