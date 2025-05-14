from flask_restful import Resource, request
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.pieza import Pieza
from app.models.orden import Orden

class PiezasHandler(Resource):

  def get(self):
    piezas = Pieza.query.all()
    piezas_js = [lo_pieza.serialize() for lo_pieza in piezas]
    return piezas_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())
    
    ordenid = data['ordenid']
    order = Orden.query.get(ordenid)

    if order.estado == 'REGISTRADO' or order.estado == 'RECHAZADO'  or order.estado == '' or order.estado is None:
      #for item in data:
      lo_pieza = Pieza(ordenid=ordenid, idvehiculo=data['idvehiculo'], idrutaprdccion=data['idrutaprdccion'], espesorval=data['espesorval'], espesor_unidad=data['espesor_unidad'], fechaentrega=data['fechaentrega'], idtpopieza=data['idtpopieza'], idtposol=data['idtposol'], created=created, update=None)
      lo_pieza.save()

      return { 'message': 'Pieza creada correctamente' }
    else:
      return {'error': 'No se puede actualizar la orden, ya que no está en estado REGISTRADO.'}, 403

  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idpieza" in data:
      lo_pieza = Pieza.query.get(data["idpieza"])
      if(lo_pieza is not None):
        if lo_pieza.orden.estado == 'REGISTRADO' or lo_pieza.orden.estado == 'RECHAZADO'  or lo_pieza.orden.estado == '' or lo_pieza.orden.estado is None:
              # Actualizar solo si el dato es proporcionado
          if "ordenid" in data:
              lo_pieza.ordenid = data["ordenid"]
          if "idvehiculo" in data:
              lo_pieza.idvehiculo = data["idvehiculo"]
          if "idrutaprdccion" in data:
              lo_pieza.idrutaprdccion = data["idrutaprdccion"]
          if "espesorval" in data:
              lo_pieza.espesorval = data["espesorval"]
          if "espesor_unidad" in data:
              lo_pieza.espesor_unidad = data["espesor_unidad"]
          if "fechaentrega" in data:
              lo_pieza.fechaentrega = data["fechaentrega"]
          if "idtpopieza" in data:
              lo_pieza.idtpopieza = data["idtpopieza"]
          if "idtposol" in data:
              lo_pieza.idtposol = data["idtposol"]

          lo_pieza.update = int(time())
          
          lo_pieza.put()
          msg = {'message': 'Pieza actualizada correctamente.'}
        else:
          msg = {'error': 'No se puede actualizar la orden, ya que no está en estado REGISTRADO.'}, 403
      else:
        msg = {'error': 'No existe la pieza a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idpieza" en payload enviado.'}, 404

    return msg
  
class PiezaIDHandler(Resource):
  @jwt_required()
  def get(self, idpieza=None):
    pieza2 = Pieza.query.get(idpieza)
    if(pieza2 is not None):
      pieza2 = pieza2.serialize()
    else:
      pieza2 = {'error': 'No existe la Pieza'}, 404
    return pieza2
