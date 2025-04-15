from flask_restful import Resource, request

from app.models.tipo_pieza import TipoPieza
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class TipoPiezasHandler(Resource):

  @jwt_required()
  def get(self):
    tipoPiezas = TipoPieza.query.all()
    tipoPieza_js = [lo_tipoPieza.serialize() for lo_tipoPieza in tipoPiezas]
    return tipoPieza_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_tipoPieza = TipoPieza(nombre=data['nombre'], created=created, update=None)
    lo_tipoPieza.save()

    return { 'message': 'Tipo de Pieza creado correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idtpopieza" in data:
      lo_tipoPieza = TipoPieza.query.get(data["idtpopieza"])
      if(lo_tipoPieza is not None):
            # Actualizar solo si el dato es proporcionado
        if "nombre" in data:
            lo_tipoPieza.nombre = data["nombre"]

        lo_tipoPieza.update = int(time())
        
        lo_tipoPieza.put()
        msg = {'message': 'Tipo de Pieza actualizado correctamente.'}
      else:
        msg = {'error': 'No existe la Tipo de Pieza a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idtpopieza" en payload enviado.'}, 404

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
