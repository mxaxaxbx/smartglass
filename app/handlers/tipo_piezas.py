from flask_restful import Resource, request

from app.models.tipo_pieza import TipoPieza

class TipoPiezasHandler(Resource):

  def get(self):
    ptypes = TipoPieza.query.all()
    ptypes = [ptype.serialize() for ptype in ptypes]
    return ptypes

  """
  Request
  [
    { 'name': 'Panoramico' },
    { 'name': 'Trasero' },
    { 'name': 'Delantero' },
    { 'name': 'Lateral' },
    { 'name': 'Central' },
  ]
  """
  def post(self):
    data = request.get_json()

    for item in data:
      ptype = TipoPieza(name=item['name'])
      ptype.save()

    return { 'message': 'part types created successfully' }
