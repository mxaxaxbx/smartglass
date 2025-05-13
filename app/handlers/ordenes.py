from flask_restful import Resource, request

from app.models.orden import Orden
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class OrdenHandler(Resource):

  @jwt_required()
  def get(self):
    ordenes = Orden.query.all()
    orden_js = [orden.serialize() for orden in ordenes]
    return orden_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())
    estado = 'REGISTRADO'

    #for item in data:
    lo_orden = Orden(fechapedido=data['fechapedido'], cliente=data['cliente'], torrecliente=data['torrecliente'], estado=estado, created=created, update=None)
    lo_orden.save()

    return { 'message': 'Orden Creado correctamente' }
    
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "ordenid" in data:
      lo_orden = Orden.query.get(data["ordenid"])
      if(lo_orden is not None):
            # Actualizar solo si el dato es proporcionado
        if "fechapedido" in data:
            lo_orden.fechapedido = data["fechapedido"]
        if "cliente" in data:
            lo_orden.cliente = data["cliente"]
        if "torrecliente" in data:
            lo_orden.torrecliente = data["torrecliente"]
        if "estado" in data:
            lo_orden.estado = data["estado"]

        lo_orden.update = int(time())
        
        lo_orden.put()
        msg = {'message': 'Orden actualizado correctamente.'}
      else:
        msg = {'error': 'No existe la orden a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "ordenid" en payload enviado.'}, 404

    return msg

class OrderIDHandler(Resource):
  @jwt_required()
  def get(self, ordenid=None):
    order2 = Orden.query.get(ordenid)
    if(order2 is not None):
      order2 = order2.serialize()
    else:
      order2 = {'error': 'No existe el usuario prueba'}, 404
    return order2
