from flask import Blueprint

from app.handlers.index import IndexHandler
from app.handlers.usuarios import UserHandler;
from app.handlers.usuarios import UserIDHandler;
from app.handlers.usuarios import UserLogin;
from app.handlers.usuarios import CurrentUserHandler;
from app.handlers.roles import RolHandler;
#from app.handlers.vehicles import VehiclesHandler
#from app.handlers.part_types import PartTypesHandler


ROUTES = [
  (IndexHandler, '/'),
  (UserLogin, '/login'),
  (UserHandler, '/usuarios'),
  (UserIDHandler, '/usuarios/<int:user_id>'),
  (CurrentUserHandler, '/usuarios/current'),  
  (RolHandler, '/roles')
  #(VehiclesHandler, '/vehicles'),
  #(PartTypesHandler, '/part_types')
]

api_bp = Blueprint('api', __name__)
