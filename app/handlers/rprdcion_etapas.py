from flask_restful import Resource, request

from app.models.rprdcion_etapa import RPrdcion_Etapas
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class RPrdcion_EtapasHandler(Resource):

  @jwt_required()
  def get(self):
    r_prd_etapas = RPrdcion_Etapas.query.all()
    r_prd_etapas_js = [lo_r_prd_etapa.serialize() for lo_r_prd_etapa in r_prd_etapas]
    return r_prd_etapas_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_r_prd_etapa = RPrdcion_Etapas(id_rutprod=data['id_rutprod'], idetapa=data['idetapa'], orden=data['orden'], created=created, update=None)
    lo_r_prd_etapa.save()

    return { 'message': 'Etapa creada correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "id_rprdcion_etapa" in data:
      lo_r_prd_etapa = RPrdcion_Etapas.query.get(data["id_rprdcion_etapa"])
      if(lo_r_prd_etapa is not None):
            # Actualizar solo si el dato es proporcionado
        if "id_rutprod" in data:
            lo_r_prd_etapa.id_rutprod = data["id_rutprod"]
        if "idetapa" in data:
            lo_r_prd_etapa.idetapa = data["idetapa"]
        if "orden" in data:
            lo_r_prd_etapa.orden = data["orden"]

        lo_r_prd_etapa.update = int(time())
        
        lo_r_prd_etapa.put()
        msg = {'message': 'Ruta de Producción / Etapa actualizada correctamente.'}
      else:
        msg = {'error': 'No existe el Ruta de Producción / Etapa a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "id_rprdcion_etapa" en payload enviado.'}, 404

    return msg
  
class RtaPrdEtpaIDHandler(Resource):
  @jwt_required()
  def get(self, id_rprdcion_etapa=None):
    r_prd_etapa = RPrdcion_Etapas.query.get(id_rprdcion_etapa)
    if(r_prd_etapa is not None):
      r_prd_etapa = r_prd_etapa.serialize()
    else:
      r_prd_etapa = {'error': 'No existe la Ruta de Producción - Etapa'}, 404
    return r_prd_etapa
  

class EtapasRtaPrdIDHandler(Resource):
  @jwt_required()
  def get(self, idrutapracion=None):
     
    r_prd_etapas = RPrdcion_Etapas.query.filter_by(id_rutprod=idrutapracion)

    r_prd_etapas_js = [lo_r_prd_etapa.serialize() for lo_r_prd_etapa in r_prd_etapas]
    return r_prd_etapas_js


