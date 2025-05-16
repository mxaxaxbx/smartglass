from flask_restful import Resource, request

from flask_jwt_extended import jwt_required
from sqlalchemy import text
from app import db  # assuming `db = SQLAlchemy(app)` is in app/__init__.py or similar


class ProductionOrdersReportHandler(Resource):

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
          o.ordenid,
          o.cliente,
          o.fechapedido AS fecha_creacion,
          COUNT(DISTINCT p.idpieza) AS total_piezas,
          o.estado AS estado_general,
          -- Porcentaje de avance: piezas terminadas / total de piezas
          ROUND(
              100.0 * COUNT(DISTINCT CASE 
                  WHEN hp.estado = 'TERMINADO' THEN p.idpieza 
              END) / NULLIF(COUNT(DISTINCT p.idpieza), 0), 
              2
          ) AS porcentaje_avance
      FROM 
          smartglass.ordenes o
      LEFT JOIN smartglass.piezas p ON p.ordenid = o.ordenid
      LEFT JOIN smartglass.procesos pr ON pr.idpieza = p.idpieza
      LEFT JOIN smartglass.historialproceso hp ON hp.idproceso = pr.idproceso
      GROUP BY 
          o.ordenid, o.fechapedido, o.estado
      ORDER BY 
          o.fechapedido DESC;
    """)
    result = db.session.execute(sql)

    return [
      {
        "ordenid": int(row[0]),
        "cliente": row[1],
        "fecha_creacion": int(row[2]),
        "total_piezas": int(row[3]),
        "estado_general": row[4],
        "porcentaje_avance": float(row[5]) if row[5] is not None else 0
      }
      for row in result
    ], 200
