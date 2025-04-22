from flask import Blueprint

from app.handlers.index import IndexHandler
from app.handlers.usuarios import UsuarioHandler, UserIDHandler, UserLogin, CurrentUserHandler;
from app.handlers.roles import RolHandler;
from app.handlers.ordenes import OrdenHandler;
from app.handlers.vehiculos import VehiculoHandler;
from app.handlers.tipo_piezas import TipoPiezasHandler;
from app.handlers.tipo_solicitudes import TipoSolicitudesHandler;
from app.handlers.rutasproduccion import RutasProduccionHandler;
from app.handlers.piezas import PiezasHandler;
from app.handlers.areas import AreasHandler;
from app.handlers.etapas import EtapasHandler;
from app.handlers.rprdcion_etapas import RPrdcion_EtapasHandler;
from app.handlers.procesos import ProcesoHandler, ProcesoIDHandler;
from app.handlers.historial_procesos import HistorialProcesoHandler, HistorialProcesoIDHandler;


ROUTES = [
  (IndexHandler, '/'),
  (UserLogin, '/login'),
  (UsuarioHandler, '/usuarios'),
  (UserIDHandler, '/usuarios/<int:user_id>'),
  (CurrentUserHandler, '/usuarios/current'),  
  (RolHandler, '/roles'),
  (OrdenHandler, '/ordenes'),
  (VehiculoHandler, '/vehiculos'),
  (TipoPiezasHandler, '/tipospiezas'),
  (TipoSolicitudesHandler, '/tipossolicitudes'),
  (RutasProduccionHandler, '/rutasproduccion'),
  (PiezasHandler, '/piezas'),
  (AreasHandler, '/areas'),
  (EtapasHandler, '/etapas'),
  (RPrdcion_EtapasHandler, '/rprdcion_etapas'),
  (ProcesoHandler, '/procesos'),
  (ProcesoIDHandler, '/procesos/<int:proceso_id>'),
  (HistorialProcesoHandler, '/historialprocesos'),
  (HistorialProcesoIDHandler, '/historialprocesos/<h_proceso_id>'),

]

api_bp = Blueprint('api', __name__)
