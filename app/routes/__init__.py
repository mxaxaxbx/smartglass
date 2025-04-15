from flask import Blueprint

from app.handlers.index import IndexHandler
from app.handlers.usuarios import UsuarioHandler;
from app.handlers.usuarios import UserIDHandler;
from app.handlers.usuarios import UserLogin;
from app.handlers.usuarios import CurrentUserHandler;
from app.handlers.roles import RolHandler;
from app.handlers.ordenes import OrdenHandler;
from app.handlers.vehiculos import VehiculoHandler;
from app.handlers.tipo_piezas import TipoPiezasHandler;


ROUTES = [
  (IndexHandler, '/'),
  (UserLogin, '/login'),
  (UsuarioHandler, '/usuarios'),
  (UserIDHandler, '/usuarios/<int:user_id>'),
  (CurrentUserHandler, '/usuarios/current'),  
  (RolHandler, '/roles'),
  (OrdenHandler, '/ordenes'),
  (VehiculoHandler, '/vehiculos'),
  (TipoPiezasHandler, '/tipos_piezas')
]

api_bp = Blueprint('api', __name__)
