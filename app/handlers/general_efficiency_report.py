from flask_restful import Resource, request

from flask_jwt_extended import jwt_required
from sqlalchemy import text
from app import db  # assuming `db = SQLAlchemy(app)` is in app/__init__.py or similar


class GeneralEfficiencyReportHandler(Resource):

  @jwt_required()
  def post(self):
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')

    # check if start or end is empty. Then return an error
    if not start or not end:
      return {'error': 'Send start and end dates'}, 400
    
    sql = text(f"""
      SELECT
        COUNT(DISTINCT pi.idpieza) AS total_piezas_recibidas,
        COUNT(DISTINCT CASE WHEN hp.estado = 'TERMINADO' THEN pi.idpieza END)::NUMERIC AS piezas_terminadas,
        COUNT(DISTINCT CASE WHEN hp.estado = 'RECHAZADO' THEN pi.idpieza END)::NUMERIC AS piezas_rechazadas,
        COUNT(DISTINCT CASE WHEN p.reproceso = TRUE THEN pi.idpieza END)::NUMERIC AS piezas_reprocesadas,
        ROUND(
            (
                COUNT(DISTINCT CASE WHEN hp.estado = 'TERMINADO' THEN pi.idpieza END)::NUMERIC * 100.0
            ) / NULLIF(COUNT(DISTINCT pi.idpieza), 0), 
            2
        ) AS eficiencia_percent
    FROM 
        smartglass.historialproceso hp
        INNER JOIN smartglass.procesos p ON p.idproceso = hp.idproceso
        INNER JOIN smartglass.piezas pi ON pi.idpieza = p.idpieza
    WHERE 
        hp.fechaingreso BETWEEN {start} AND {end};
    """)
    result = db.session.execute(sql)

    return [
      {
        "total_piezas_recibidas": int(row[0]),
        "piezas_terminadas": int(row[1]),
        "piezas_rechazadas": int(row[2]),
        "piezas_reprocesadas": int(row[3]),
        "eficiencia_percent": float(row[4]),
      }
      for row in result
    ], 200
