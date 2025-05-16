from flask_restful import Resource, request

from flask_jwt_extended import jwt_required
from sqlalchemy import text
from app import db  # assuming `db = SQLAlchemy(app)` is in app/__init__.py or similar


class EfficiencyReportHandler(Resource):

  @jwt_required()
  def post(self):
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')

    # check if start or end is empty. Then return an error
    if not start or not end:
      return {'error': 'Send start and end dates'}, 400
    
    sql = text(f"""
    -- Count of pieces received by each stage during a specific month
    SELECT 
        e.idetapa,
        e.nombre AS nombre_etapa,
        a.idarea,
        a.nombre AS nombre_area,
        COUNT(DISTINCT pi.idpieza) AS total_piezas,
        COUNT(distinct case when hp.estado = 'TERMINADO' then pi.idpieza end)::numeric as piezas_terminadas,
        COUNT(DISTINCT CASE WHEN hp.estado = 'RECHAZADO' THEN pi.idpieza END)::NUMERIC as piezas_rechazadas,
        COUNT(DISTINCT CASE WHEN p.reproceso = true THEN pi.idpieza END)::NUMERIC AS piezas_reprocesadas
    FROM 
        smartglass.etapas e 
        INNER JOIN smartglass.areas a ON a.idarea = e.areaid
        INNER JOIN smartglass.historialproceso hp ON hp.idetapa = e.idetapa
        INNER JOIN smartglass.procesos p ON p.idproceso = hp.idproceso
        INNER JOIN smartglass.piezas pi ON pi.idpieza = p.idpieza
    WHERE
        hp.fechaingreso BETWEEN {start} AND {end}
    GROUP BY 
        e.idetapa, 
        e.nombre,
        a.idarea,
        a.nombre
    ORDER BY 
        a.nombre, 
        e.nombre;
    """)
    result = db.session.execute(sql)

    return [
      {
        "idetapa": row[0],
        "nombre_etapa": row[1],
        "idarea": row[2],
        "nombre_area": row[3],
        "total_piezas": row[4],
        "piezas_terminadas": float(row[5]),
        "piezas_rechazadas": float(row[6]),
        "piezas_reprocesadas": float(row[7]),
      }
      for row in result
    ], 200
