from flask_restful import Resource, request
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.historial_proceso import HistorialProceso
from app.models.usuario import Usuario

class HistorialProcesoHandler(Resource):

  def get(self):
    hitorial_procesos = HistorialProceso.query.all()
    hitorial_procesos_js = [lo_hproceso.serialize() for lo_hproceso in hitorial_procesos]
    return hitorial_procesos_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_hproceso = HistorialProceso(estado=data['estado'], fechaingreso=data['fechaingreso'], fechasalida=data['fechasalida'], idetapa=data['idetapa'], idproceso=data['idproceso'], idusuario=data['idusuario'], notas=data['notas'], created=created, update=None)
    try:
      lo_hproceso.save()
      return { 'message': 'Historial de proceso creado correctamente' }
    except Exception as e:
      return {'error': str(e)}, 500

  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idhistorialprocso" in data:
      lo_hproceso = HistorialProceso.query.get(data["idhistorialprocso"])
      if(lo_hproceso is not None):
            # Actualizar solo si el dato es proporcionado
        if "estado" in data:
            lo_hproceso.estado = data["estado"]
        if "fechaingreso" in data:
            lo_hproceso.fechaingreso = data["fechaingreso"]
        if "fechasalida" in data:
            lo_hproceso.fechasalida = data["fechasalida"]
        if "idetapa" in data:
            lo_hproceso.idetapa = data["idetapa"]
        if "idproceso" in data:
            lo_hproceso.idproceso = data["idproceso"]
        if "idusuario" in data:
            lo_hproceso.idusuario = data["idusuario"]
        if "notas" in data:
            lo_hproceso.notas = data["notas"]

        lo_hproceso.update = int(time())
        
        lo_hproceso.put()
        msg = {'message': 'Historial de proceso actualizada correctamente.'}
      else:
        msg = {'error': 'No existe el Historial de Proceso a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idhistorialprocso" en payload enviado.'}, 404

    return msg
  
class HistorialProcesoIDHandler(Resource):
  @jwt_required()
  def get(self, h_proceso_id=None):
    lo_hproceso = HistorialProceso.query.get(h_proceso_id)
    if(lo_hproceso is not None):
      h_proceso_js = lo_hproceso.serialize()
    else:
      h_proceso_js = {'error': 'No existe el Historial de Proceso asociado al Id enviado'}, 404
    return h_proceso_js
  
class HistorialProcesoUserIDHandler(Resource):
  @jwt_required()
  def get(self, user_id=None):  
    lo_user = Usuario.query.get(user_id)
    if(lo_user is not None):
      hitorial_procesos_js = [lo_hproceso.serialize() 
                              for lo_etapa in lo_user.area.etapas
                                for lo_hproceso in lo_etapa.hsProcesos]
      
    else:
      hitorial_procesos_js = {'error': 'No existe el procesos de peizas asociados al usuario'}, 404
    return hitorial_procesos_js

class HistorialProcesoTerminarHandler(Resource):
  @jwt_required()
  def post(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idhistorialprocso" in data:
      lo_hproceso = HistorialProceso.query.get(data["idhistorialprocso"])
      if(lo_hproceso is not None):
        #Actualizo el historial de la orden a terminado      
        if "notas" in data:
          lo_hproceso.notas = data["notas"]

        lo_hproceso.estado = 'TERMINADO'
        lo_hproceso.fechasalida = int(time())
        lo_hproceso.update = int(time())
        
        userid = get_jwt_identity()
        lo_hproceso.idusuario = userid
        
        lo_hproceso.put()

        #Busco las etpas asociados a la pieza
        rprdcion_etapas = lo_hproceso.proceso.pieza.rutaprdccion.rprdcion_etapas
        rprdcion_etapa_act = dict()
        rprdcion_etapa_next = dict()

        for lo_rprdcion_etapa in rprdcion_etapas:
          if lo_rprdcion_etapa.idetapa == lo_hproceso.idetapa and lo_rprdcion_etapa.id_rutprod == lo_hproceso.proceso.pieza.idrutaprdccion:
            rprdcion_etapa_act = lo_rprdcion_etapa
            break
        
        if rprdcion_etapa_act.etapafinal == True:
          # Busco y actualizo el estado del proceso
          lo_proceso = lo_hproceso.proceso
          lo_proceso.estado = 'TERMINADO'
          lo_proceso.fechasalida = int(time())
          lo_proceso.update = int(time())
          lo_proceso.put()

          # Busco y actualizo el estado de la pieza
          lo_pieza = lo_hproceso.proceso.pieza
          lo_pieza.estado = 'TERMINADO'
          lo_pieza.update = int(time())
          lo_pieza.put()

          # Busco y actualizo el estado de la orden
          lo_orden = lo_hproceso.proceso.pieza.orden
          piezas = lo_orden.piezas

          l_piezas_terminadas = False
          for lo_pieza_t in piezas:
            if lo_pieza_t.estado == 'TERMINADO':
              l_piezas_terminadas = True
            else:
              l_piezas_terminadas = False
              break
          
          if l_piezas_terminadas == True:
            lo_orden.estado = 'TERMINADO'
            lo_orden.update = int(time())
            lo_orden.put()

        else:
          #Busco la etapa asociada al historial del proceso
          l_is_ok = False
          orden = rprdcion_etapa_act.orden + 1

          for lo_rprdcion_etapa in rprdcion_etapas:
            if lo_rprdcion_etapa.orden == orden and lo_rprdcion_etapa.id_rutprod == lo_hproceso.proceso.pieza.idrutaprdccion:
              rprdcion_etapa_next = lo_rprdcion_etapa              
              l_is_ok = True
              break
          
          # Inserto el registro para que se vea en la siguiente etapa
          if l_is_ok == True:
            lo_hproceso_new = HistorialProceso(estado='REGISTRADO', fechaingreso=int(time()), fechasalida=None, idetapa=rprdcion_etapa_next.idetapa, idproceso=lo_hproceso.idproceso, idusuario=userid, notas=None, created=int(time()), update=None)
            lo_hproceso_new.save()
        
        #msg = rprdcion_etapa_next.serialize()
        #msg = {'o': orden, 'entro': ent}
        msg = {'message': 'Historial de proceso actualizado correctamente.'}
      else:
        msg = {'error': 'No existe el Historial de Proceso a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idhistorialprocso" en payload enviado.'}, 404

    return msg
  

