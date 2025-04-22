from flask_restful import Resource, request

from app.models.area import Area
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class AreasHandler(Resource):

  @jwt_required()
  def get(self):
    areas = Area.query.all()
    areas_js = [lo_area.serialize() for lo_area in areas]
    return areas_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_area = Area(nombre=data['nombre'], created=created, update=None)
    lo_area.save()

    return { 'message': 'Area creada correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idarea" in data:
      lo_area = Area.query.get(data["idarea"])
      if(lo_area is not None):
            # Actualizar solo si el dato es proporcionado
        if "nombre" in data:
            lo_area.nombre = data["nombre"]

        lo_area.update = int(time())
        
        lo_area.put()
        msg = {'message': 'Area actualizada correctamente.'}
      else:
        msg = {'error': 'No existe el Area a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idarea" en payload enviado.'}, 404

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
