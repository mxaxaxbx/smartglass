from flask import Blueprint

from app.handlers.index import IndexHandler
from app.handlers.vehicles import VehiclesHandler
from app.handlers.part_types import PartTypesHandler
from app.handlers.usuarios import UserHandler;
from app.handlers.usuarios import UserIDHandler;


ROUTES = [
  (IndexHandler, '/'),
  (VehiclesHandler, '/vehicles'),
  (UserHandler, '/usuarios'),
  (UserIDHandler, '/usuarios/<int:user_id>'),
  (PartTypesHandler, '/part_types')
]

api_bp = Blueprint('api', __name__)
