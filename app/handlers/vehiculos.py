from flask_restful import Resource, request
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.vehiculo import Vehiculo

class VehiculoHandler(Resource):

  def get(self):
    vehiculos = Vehiculo.query.all()
    vehiculos_js = [vehiculo.serialize() for vehiculo in vehiculos]
    return vehiculos_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_vehiculo = Vehiculo(marca=data['marca'], modelo=data['modelo'], year_ini_prod=data['year_ini_prod'], year_fin_prod=data['year_fin_prod'], created=created, update=None)
    lo_vehiculo.save()

    return { 'message': 'Vehiculo creado correctamente' }

  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idvehiculo" in data:
      lo_vehiculo = Vehiculo.query.get(data["idvehiculo"])
      if(lo_vehiculo is not None):
            # Actualizar solo si el dato es proporcionado
        if "marca" in data:
            lo_vehiculo.marca = data["marca"]
        if "modelo" in data:
            lo_vehiculo.modelo = data["modelo"]
        if "year_ini_prod" in data:
            lo_vehiculo.year_ini_prod = data["year_ini_prod"]
        if "year_fin_prod" in data:
            lo_vehiculo.year_fin_prod = data["year_fin_prod"]

        lo_vehiculo.update = int(time())
        
        lo_vehiculo.put()
        msg = {'message': 'Vehiculo actualizado correctamente.'}
      else:
        msg = {'error': 'No existe el vehiculo a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idvehiculo" en payload enviado.'}, 404

    return msg
  

class VehiculoIDHandler(Resource):
  @jwt_required()
  def get(self, idvehiculo=None):
    vehiculo2 = Vehiculo.query.get(idvehiculo)
    if(vehiculo2 is not None):
      vehiculo2 = vehiculo2.serialize()
    else:
      vehiculo2 = {'error': 'No existe el usuario prueba'}, 404
    return vehiculo2
  