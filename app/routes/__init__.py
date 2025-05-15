from flask import Blueprint

from app.handlers.index import IndexHandler
from app.handlers.usuarios import UsuarioHandler, UserIDHandler, UserLogin, CurrentUserHandler;
from app.handlers.roles import RolHandler, RolIDHandler;
from app.handlers.ordenes import OrdenHandler, OrderIDHandler, OrderIDEstadoHandler, AprobarOrdenHandler;
from app.handlers.vehiculos import VehiculoHandler, VehiculoIDHandler;
from app.handlers.tipo_piezas import TipoPiezasHandler, TpoPiezaIDHandler;
from app.handlers.tipo_solicitudes import TipoSolicitudesHandler, TpoSolIDHandler;
from app.handlers.rutasproduccion import RutasProduccionHandler, RtaProdIDHandler;
from app.handlers.piezas import PiezasHandler, PiezaIDHandler;
from app.handlers.areas import AreasHandler, AreaIDHandler;
from app.handlers.etapas import EtapasHandler, EtapaIDHandler;
from app.handlers.rprdcion_etapas import RPrdcion_EtapasHandler, RtaPrdEtpaIDHandler, EtapasRtaPrdIDHandler;
from app.handlers.procesos import ProcesoHandler, ProcesoIDHandler;
from app.handlers.historial_procesos import HistorialProcesoHandler, HistorialProcesoIDHandler, HistorialProcesoUserIDHandler;


ROUTES = [
  (IndexHandler, '/'),
  (UserLogin, '/login'),
  (UsuarioHandler, '/usuarios'),
  (UserIDHandler, '/usuarios/<int:user_id>'),
  (CurrentUserHandler, '/usuarios/current'),
  (RolHandler, '/roles'),
  (RolIDHandler, '/roles/<int:idrol>'),
  (OrdenHandler, '/ordenes'),
  (OrderIDHandler, '/ordenes/<int:ordenid>'),
  (OrderIDEstadoHandler, '/ordenes/estado'),
  (AprobarOrdenHandler, '/ordenes/apoprobar'),
  (VehiculoHandler, '/vehiculos'),
  (VehiculoIDHandler, '/vehiculos/<int:idvehiculo>'),
  (TipoPiezasHandler, '/tipospiezas'),
  (TpoPiezaIDHandler, '/tipospiezas/<int:idtpopieza>'),
  (TipoSolicitudesHandler, '/tipossolicitudes'),
  (TpoSolIDHandler, '/tipossolicitudes/<int:idtposol>'),
  (RutasProduccionHandler, '/rutasproduccion'),
  (RtaProdIDHandler, '/rutasproduccion/<int:idrutapracion>'),
  (EtapasRtaPrdIDHandler, '/rutasproduccion/<int:idrutapracion>/etapas'),
  (PiezasHandler, '/piezas'),
  (PiezaIDHandler, '/piezas/<int:idpieza>'),
  (AreasHandler, '/areas'),
  (AreaIDHandler, '/areas/<int:idarea>'),
  (EtapasHandler, '/etapas'),
  (EtapaIDHandler, '/etapas/<int:idetapa>'),
  (RPrdcion_EtapasHandler, '/rprdcion_etapas'),
  (RtaPrdEtpaIDHandler, '/rprdcion_etapas/<int:id_rprdcion_etapa>'),
  (ProcesoHandler, '/procesos'),
  (ProcesoIDHandler, '/procesos/<int:proceso_id>'),
  (HistorialProcesoHandler, '/historialprocesos'),
  (HistorialProcesoIDHandler, '/historialprocesos/<h_proceso_id>'),
  (HistorialProcesoUserIDHandler, '/historialprocesos/usuario/<int:user_id>'),

]

api_bp = Blueprint('api', __name__)
