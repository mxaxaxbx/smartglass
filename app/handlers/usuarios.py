from flask_restful import Resource, request

from app.models.user import User
from time import time

class UserHandler(Resource):

  def get(self):
    users = User.query.all()
    users2 = [user.serialize() for user in users]
    return users2
  
  def put(self):
    users = User.query.all()

  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    user = User(primer_nombre=data['primer_nombre'], segundo_nombre=data['segundo_nombre'], 
                  primer_apellido=data['primer_apellido'], segundo_apellido=data['segundo_apellido'], active=data['active'],
                    superuser=data['superuser'], created=created, update=None, lastlogin=None, 
                    email=data['email'], password=data['password'])
    user.save()

    return { 'message': 'Usuario created successfully' }

class UserIDHandler(Resource):

  def get(self, user_id=None):
    users2 = User.query.get(user_id)
    if(users2 is not None):
      users2 = users2.serialize()
    else:
      users2 = {'error': 'No existe el usuario'}, 404
    return users2


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

  """
  def post(self):
    data = request.get_json()

    for item in data:
      vehicle = Vehicle(brand=item['brand'], model=item['model'], year=item['year'])
      vehicle.save()

    return { 'message': 'Vehicles created successfully' }
    """
