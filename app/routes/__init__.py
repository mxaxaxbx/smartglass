from flask import Blueprint

from app.handlers.index import IndexHandler
from app.handlers.vehicles import VehiclesHandler
from app.handlers.part_types import PartTypesHandler


ROUTES = [
  (IndexHandler, '/'),
  (VehiclesHandler, '/vehicles'),
  (PartTypesHandler, '/part_types')
]

api_bp = Blueprint('api', __name__)
