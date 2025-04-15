from flask_restful import Resource, request

from app.models.orden import Orden
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class OrdenHandler(Resource):

  @jwt_required()
  def get(self):
    ordenes = Orden.query.all()
    orden = [orden.serialize() for orden in ordenes]
    return orden
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "ordenid" in data:
      l_orden = Orden.query.get(data["ordenid"])
      if(l_orden is not None):
            # Actualizar solo si el dato es proporcionado
        if "fechapedido" in data:
            l_orden.fechapedido = data["fechapedido"]
        if "cliente" in data:
            l_orden.cliente = data["cliente"]
        if "torrecliente" in data:
            l_orden.torrecliente = data["torrecliente"]

        l_orden.update = int(time())
        
        l_orden.put()
        msg = {'message': 'Orden actualizado correctamente.'}
      else:
        msg = {'error': 'No existe la orden a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "ordenid" en payload enviado.'}, 404

    return msg

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    orden = Orden(fechapedido=data['fechapedido'], cliente=data['cliente'], torrecliente=data['torrecliente'], created=created, update=None)
    orden.save()

    return { 'message': 'Orden Creado correctamente' }
  

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
