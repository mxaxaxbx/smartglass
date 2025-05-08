from flask_restful import Resource, request

from app.models.tipo_solicitud import TipoSolicitud
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class TipoSolicitudesHandler(Resource):

  @jwt_required()
  def get(self):
    tipoSolicitudes = TipoSolicitud.query.all()
    tipoSolicitud_js = [lo_tipoSolicitud.serialize() for lo_tipoSolicitud in tipoSolicitudes]
    return tipoSolicitud_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_tipoSolicitud = TipoSolicitud(nombre=data['nombre'], created=created, update=None)
    lo_tipoSolicitud.save()

    return { 'message': 'Tipo de Solicitud creado correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idtposol" in data:
      lo_tipoSolicitud = TipoSolicitud.query.get(data["idtposol"])
      if(lo_tipoSolicitud is not None):
            # Actualizar solo si el dato es proporcionado
        if "nombre" in data:
            lo_tipoSolicitud.nombre = data["nombre"]

        lo_tipoSolicitud.update = int(time())
        
        lo_tipoSolicitud.put()
        msg = {'message': 'Tipo de Solicitud actualizado correctamente.'}
      else:
        msg = {'error': 'No existe la Tipo de Solicitud a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idtposol" en payload enviado.'}, 404

    return msg
  
class TpoSolIDHandler(Resource):
  @jwt_required()
  def get(self, idtposol=None):
    tpoSol2 = TipoSolicitud.query.get(idtposol)
    if(tpoSol2 is not None):
      tpoSol2 = tpoSol2.serialize()
    else:
      tpoSol2 = {'error': 'No existe el Tipo de Solicitud'}, 404
    return tpoSol2
