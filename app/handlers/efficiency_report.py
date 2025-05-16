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
        ROUND(
          COUNT(distinct case when hp.estado = 'TERMINADO' then pi.idpieza end)::numeric /
          nullif(count(distinct pi.idpieza), 0)::numeric * 100,
          2
        ) as porcentaje_terminadas,
        ROUND(
            COUNT(DISTINCT CASE WHEN hp.estado = 'RECHAZADA' THEN pi.idpieza END)::NUMERIC / 
            NULLIF(COUNT(DISTINCT pi.idpieza), 0)::NUMERIC * 100, 
            2
        ) AS porcentaje_rechazadas,
        ROUND(
            COUNT(DISTINCT CASE WHEN p.reproceso = true THEN pi.idpieza END)::NUMERIC / 
            NULLIF(COUNT(DISTINCT pi.idpieza), 0)::NUMERIC * 100, 
            2
        ) AS porcentaje_reprocesadas
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
        "porcentaje_terminadas": float(row[5]),
        "porcentaje_rechazadas": float(row[6]),
        "porcentaje_reprocesadas": float(row[7]),
      }
      for row in result
    ], 200
