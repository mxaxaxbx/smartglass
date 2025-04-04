from flask_restful import Resource, request

from app.models.user import User
from time import time
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class UserHandler(Resource):

  @jwt_required()
  def get(self):
    users = User.query.all()
    users2 = [user.serialize() for user in users]
    return users2
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "userid" in data:
      l_user = User.query.get(data["userid"])
      if(l_user is not None):
            # Actualizar solo si el dato es proporcionado
        if "primer_nombre" in data:
            l_user.primer_nombre = data["primer_nombre"]
        if "segundo_nombre" in data:
            l_user.segundo_nombre = data["segundo_nombre"]
        if "primer_apellido" in data:
            l_user.primer_apellido = data["primer_apellido"]
        if "segundo_apellido" in data:
            l_user.segundo_apellido = data["segundo_apellido"]
        if "email" in data:
            l_user.email = data["email"]
        if "password" in data:
            l_user.password = self.hash_password(data['password'])
        if "idrol" in data:
            l_user.idrol = data["idrol"]
        if "idarea" in data:
            l_user.idarea = data["idarea"]
        if "active" in data:
            l_user.active = data["active"]
        if "superuser" in data:
            l_user.superuser = data["superuser"]

        l_user.update = int(time())
        
        l_user.put()
        msg = {'message': 'Usuario actualizado correctamente.'}
      else:
        msg = {'error': 'No existe el usuario a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "userid" en payload enviado.'}, 404

    return msg

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

class CurrentUserHandler(Resource):
  @jwt_required()
  def get(self):
    userid = get_jwt_identity()
    users2 = User.query.get(userid)
    if(users2 is not None):
      users2 = users2.serialize()
    else:
      users2 = {'error': 'No existe el usuario logueado.'}, 404
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
        user.lastlogin = int(time())
        user.put()
        rt_data = { 'access_token': access_token}
      else:
        rt_data = { 'message': "Contraseña incorrecta" }, 401

    else:
      rt_data = { 'message': "Usuario no existe" }, 401

    return rt_data
  
  def verify_password(self, password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
  