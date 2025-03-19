from flask_restful import Resource, request

from app.models.user import User
from time import time
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required



class UserHandler(Resource):

  @jwt_required()
  def get(self):
    users = User.query.all()
    users2 = [user.serialize() for user in users]
    return users2
  
  @jwt_required()
  def put(self):
    users = User.query.all()
    return { 'message': 'User update successfully' }

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())
    hashed_password = self.hash_password(data['password'])

    #for item in data:
    user = User(primer_nombre=data['primer_nombre'], segundo_nombre=data['segundo_nombre'], 
                  primer_apellido=data['primer_apellido'], segundo_apellido=data['segundo_apellido'], active=data['active'],
                    superuser=data['superuser'], created=created, update=None, lastlogin=None, 
                    email=data['email'], password=hashed_password)
    user.save()

    return { 'message': 'User created successfully' }
  
  def hash_password(self, password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()
  

class UserIDHandler(Resource):
  @jwt_required()
  def get(self, user_id=None):
    users2 = User.query.get(user_id)
    if(users2 is not None):
      users2 = users2.serialize()
    else:
      users2 = {'error': 'No existe el usuario prueba'}, 404
    return users2
  

class UserLogin(Resource):

  def post(self):

    data = request.get_json()
    email = data['email']
    password = data['password']

    users = User.query.filter_by(email=email)

    isValid = False

    if(users.count() > 0):
      user = users[0]

      isValid = self.verify_password(password, user.password)

      if(isValid):
        access_token = create_access_token(identity=str(user.userid))
        rt_data = { 'access_token': access_token}
      else:
        rt_data = { 'message': "Contraseña incorrecta" }, 401

    else:
      rt_data = { 'message': "Usuario no existe" }, 401

    return rt_data
  
  def verify_password(self, password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
  
