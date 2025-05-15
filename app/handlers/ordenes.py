from flask_restful import Resource, request

from app.models.orden import Orden
from app.models.pieza import Pieza
from app.models.proceso import Proceso
from app.models.historial_proceso import HistorialProceso

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

    return { 'message': 'Orden Creado correctamente',
             'ordenid': str(lo_orden.ordenid)  }
    
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "ordenid" in data:
      lo_orden = Orden.query.get(data["ordenid"])
      if(lo_orden is not None):
        if lo_orden.estado == 'REGISTRADO' or lo_orden.estado == 'RECHAZADO'  or lo_orden.estado == '' or lo_orden.estado is None:
            # Actualizar solo si el dato es proporcionado
          if "fechapedido" in data:
              lo_orden.fechapedido = data["fechapedido"]
          if "cliente" in data:
              lo_orden.cliente = data["cliente"]
          if "torrecliente" in data:
              lo_orden.torrecliente = data["torrecliente"]
          
          lo_orden.estado = 'REGISTRADO'

          lo_orden.update = int(time())
          
          lo_orden.put()
          msg = {'message': 'Orden actualizado correctamente.'}
        else:
          msg = {'error': 'No se puede actualizar la orden, ya que no está en estado REGISTRADO.'}, 403
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

class OrderIDEstadoHandler(Resource):
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "ordenid" in data:
      lo_orden = Orden.query.get(data["ordenid"])
      if(lo_orden is not None):
        # Actualizar solo si el dato es proporcionado
        if "estado" in data:
          lo_orden.estado = data["estado"]

        lo_orden.update = int(time())
          
        lo_orden.put()
        msg = {'message': 'Estado de Orden actualizado correctamente.'}
      else:
        msg = {'error': 'No existe la orden a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "ordenid" en payload enviado.'}, 404

    return msg
  
class AprobarOrdenHandler(Resource):
  @jwt_required()
  def post(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "ordenid" in data:
      lo_orden = Orden.query.get(data["ordenid"])
      if(lo_orden is not None):
        # Busco usuario        
        userid = get_jwt_identity()
        
        # Actualizado el estado de la orden a EN_PROCESO
        lo_orden.estado = 'EN_PROCESO'
        lo_orden.update = int(time())
        l_today = int(time())        
        lo_orden.put()
        
        # Busco y actualizo las piezas de la orden
        piezas = Pieza.query.filter_by(ordenid=data["ordenid"]).all()
        for lo_pieza in piezas:
          # Actualizar solo si el dato es proporcionado
          if "fechaentrega" in data:
            lo_pieza.fechaentrega = data["fechaentrega"]
          
          lo_pieza.estado = 'EN_PROCESO'
          lo_pieza.put()
           
          # Crear proceso de la pieza
          lo_proceso = Proceso(estado='EN_PROCESO', fechainicial=l_today, idpieza=lo_pieza.idpieza, created=l_today, update=None)
          lo_proceso.save()
          
          # Obetener la etapa de la pieza
          etapas_rta = lo_pieza.rutaprdccion.rprdcion_etapas          
          etapas_rta.sort(key=lambda lo_rprdcion_etapa: lo_rprdcion_etapa.orden)
        
          # Crear el historial de la pieza
          lo_historial = HistorialProceso(estado='REGISTRADO', fechaingreso=l_today, idetapa=etapas_rta[0].idetapa, idproceso=lo_proceso.idproceso, idusuario=userid, created=l_today, update=None)
          lo_historial.save()
                      
          msg = {'message': 'Orden aprobada para paso a producción correctamente.'}
        
        
      else:
        msg = {'error': 'No existe la orden a aprobar.'}, 404
    else:
      msg = {'error': 'No existe atributo "ordenid" en payload enviado.'}, 404

    return msg