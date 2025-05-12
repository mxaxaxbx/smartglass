from flask_restful import Resource, request

from app.models.rutaproduccion import RutaProduccion
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class RutasProduccionHandler(Resource):

  @jwt_required()
  def get(self):
    rutasproduccion = RutaProduccion.query.all()
    rutasproduccion_js = [lo_rutaprod.serialize() for lo_rutaprod in rutasproduccion]
    return rutasproduccion_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_rutaprod = RutaProduccion(nombre=data['nombre'], created=created, update=None)
    lo_rutaprod.save()

    return { 'message': 'Ruta de Producción creada correctamente',
             'id_rutaprod': lo_rutaprod.idrutaprdcion }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idrutaprdcion" in data:
      lo_rutaprod = RutaProduccion.query.get(data["idrutaprdcion"])
      if(lo_rutaprod is not None):
            # Actualizar solo si el dato es proporcionado
        if "nombre" in data:
            lo_rutaprod.nombre = data["nombre"]

        lo_rutaprod.update = int(time())
        
        lo_rutaprod.put()
        msg = {'message': 'Ruta de Producción actualizado correctamente.'}
      else:
        msg = {'error': 'No existe la Ruta de Producción a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idrutapracion" en payload enviado.'}, 404

    return msg
  
class RtaProdIDHandler(Resource):
  @jwt_required()
  def get(self, idrutapracion=None):
    rutaprod = RutaProduccion.query.get(idrutapracion)
    if(rutaprod is not None):
      rutaprod = rutaprod.serialize()
    else:
      rutaprod = {'error': 'No existe la ruta de producción'}, 404
    return rutaprod
