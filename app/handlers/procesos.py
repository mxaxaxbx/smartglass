from flask_restful import Resource, request
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.proceso import Proceso
from app.models.historial_proceso import HistorialProceso

class ProcesoHandler(Resource):

  def get(self):
    procesos = Proceso.query.all()
    procesos_js = [lo_proceso.serialize() for lo_proceso in procesos]
    return procesos_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())
    
    #for item in data:
    lo_proceso = Proceso(idpieza=data['idpieza'], fechainicial=data['fechainicial'], fechafinal=data['fechafinal'], estado=data['estado'], notas=data['notas'], reproceso=data['reproceso'], created=created, update=None)
    try:
      lo_proceso.save()
      return { 'message': 'Proceso creado correctamente' }
    except Exception as e:
      return {'error': str(e)}, 500


  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idproceso" in data:
      lo_proceso = Proceso.query.get(data["idproceso"])
      if(lo_proceso is not None):
            # Actualizar solo si el dato es proporcionado
        if "idpieza" in data:
            lo_proceso.idpieza = data["idpieza"]
        if "fechainicial" in data:
            lo_proceso.fechainicial = data["fechainicial"]
        if "fechafinal" in data:
            lo_proceso.fechafinal = data["fechafinal"]
        if "estado" in data:
            lo_proceso.estado = data["estado"]
        if "notas" in data:
            lo_proceso.notas = data["notas"]
        if "reproceso" in data:
            lo_proceso.reproceso = data["reproceso"]

        lo_proceso.update = int(time())
        
        lo_proceso.put()
        msg = {'message': 'Proceso actualizada correctamente.'}
      else:
        msg = {'error': 'No existe el Proceso a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idproceso" en payload enviado.'}, 404

    return msg
  
class ProcesoIDHandler(Resource):
  @jwt_required()
  def get(self, proceso_id=None):
    lo_proceso = Proceso.query.get(proceso_id)
    if(lo_proceso is not None):
      proceso_js = lo_proceso.serialize()
    else:
      proceso_js = {'error': 'No existe el Proceso asociado al Id enviado'}, 404
    return proceso_js
  
class ProcesoReproHandler(Resource):
  @jwt_required()
  def post(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idproceso" in data and "idetapa" in data:
      lo_proceso = Proceso.query.get(data["idproceso"])
      if(lo_proceso is not None):
        lo_proceso.reproceso = True
        if "notas" in data:
            lo_proceso.notas = data["notas"]
            
        lo_proceso.update = int(time())
        lo_proceso.put()
        
        hprocesos = lo_proceso.historialproceso
        if hprocesos is not None:
          # Actualizar el estado de la historia de proceso a "REPROCESO"
          hprocesos.sort(key=lambda lo_hproceso: lo_hproceso.fechaingreso, reverse=True)
          hproceso = hprocesos[0]
          
          hproceso.estado = 'REPROCESO'
          hproceso.fechasalida = int(time())
          if "notas" in data:
              hproceso.notas = data["notas"]
              
          hproceso.update = int(time())
          hproceso.put()
                    
          # Crear nuevo historial de proceso
          lo_historial = HistorialProceso(estado='REGISTRADO', fechaingreso=int(time()), fechasalida=None, idetapa=data["idetapa"], idproceso=lo_proceso.idproceso, idusuario=get_jwt_identity(), notas=None, created=int(time()), update=None)
          lo_historial.save()
          
        msg = {'message': 'Proceso Reprocesado correctamente.'}
      else:
        msg = {'error': 'No existe el Proceso a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idproceso" en payload enviado.'}, 404

    return msg
  
class ProcesoRchzrHandler(Resource):
  @jwt_required()
  def post(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idproceso" in data:
      lo_proceso = Proceso.query.get(data["idproceso"])
      if(lo_proceso is not None):
            # Actualizar solo si el dato es proporcionado
        if "idpieza" in data:
            lo_proceso.idpieza = data["idpieza"]
        if "fechainicial" in data:
            lo_proceso.fechainicial = data["fechainicial"]
        if "fechafinal" in data:
            lo_proceso.fechafinal = data["fechafinal"]
        if "estado" in data:
            lo_proceso.estado = data["estado"]
        if "notas" in data:
            lo_proceso.notas = data["notas"]
        if "reproceso" in data:
            lo_proceso.reproceso = data["reproceso"]

        lo_proceso.update = int(time())
        
        lo_proceso.put()
        msg = {'message': 'Proceso actualizada correctamente.'}
      else:
        msg = {'error': 'No existe el Proceso a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idproceso" en payload enviado.'}, 404

    return msg

