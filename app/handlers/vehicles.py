from flask_restful import Resource, request

from app.models.vehicles import Vehicle

class VehiclesHandler(Resource):

  def get(self):
    vehicles = Vehicle.query.all()
    vehicles = [vehicle.serialize() for vehicle in vehicles]
    return vehicles

  """
  Request
  [
    { 'brand': 'Toyota', 'model': 'Corolla', 'year': 2019 },
    { 'brand': 'Toyota', 'model': 'Yaris', 'year': 2019 },
    { 'brand': 'Toyota', 'model': 'Hilux', 'year': 2019 },
    { 'brand': 'Toyota', 'model': 'Fortuner', 'year': 2019 },
    { 'brand': 'Toyota', 'model': 'Prado', 'year': 2019 },
  ]
  """
  def post(self):
    data = request.get_json()

    for item in data:
      vehicle = Vehicle(brand=item['brand'], model=item['model'], year=item['year'])
      vehicle.save()

    return { 'message': 'Vehicles created successfully' }
