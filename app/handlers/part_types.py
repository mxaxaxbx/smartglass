from flask_restful import Resource, request

from app.models.part_types import PartTypes

class PartTypesHandler(Resource):

  def get(self):
    ptypes = PartTypes.query.all()
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
      ptype = PartTypes(name=item['name'])
      ptype.save()

    return { 'message': 'part types created successfully' }
