from flask_restful import Resource, request

from app.models.etapa import Etapa
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class EtapasHandler(Resource):

  @jwt_required()
  def get(self):
    etapas = Etapa.query.all()
    etapas_js = [lo_etapas.serialize() for lo_etapas in etapas]
    return etapas_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_etapa = Etapa(areaid=data['areaid'], nombre=data['nombre'], etapafinal=data['etapafinal'], created=created, update=None)
    lo_etapa.save()

    return { 'message': 'Etapa creada correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idetapa" in data:
      lo_etapa = Etapa.query.get(data["idetapa"])
      if(lo_etapa is not None):
            # Actualizar solo si el dato es proporcionado
        if "areaid" in data:
            lo_etapa.areaid = data["areaid"]
        if "nombre" in data:
            lo_etapa.nombre = data["nombre"]
        if "etapafinal" in data:
            lo_etapa.etapafinal = data["etapafinal"]

        lo_etapa.update = int(time())
        
        lo_etapa.put()
        msg = {'message': 'Etapa actualizada correctamente.'}
      else:
        msg = {'error': 'No existe el Etapa a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idetapa" en payload enviado.'}, 404

    return msg
  
"""class UserIDHandler(Resource):
  @jwt_required()
  def get(self, user_id=None):
    users2 = User.query.get(user_id)
    if(users2 is not None):
      users2 = users2.serialize()
    else:
      users2 = {'error': 'No existe el usuario prueba'}, 404
    return users2
"""
