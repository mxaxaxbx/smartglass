from flask import Blueprint

from app.handlers.index import Index
from app.handlers.vehicles import Vehicles


ROUTES = [
  (Index, '/'),
  (Vehicles, '/vehicles'),
]

api_bp = Blueprint('api', __name__)
