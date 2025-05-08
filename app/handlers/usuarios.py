from flask_restful import Resource, request

from app.models.usuario import Usuario
from time import time
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

class UsuarioHandler(Resource):

  @jwt_required()
  def get(self):
    #users = Usuario.query.all()
    users =  Usuario.query.filter_by(active=True).all()
    users_js = [lo_user.serialize() for lo_user in users]
    return users_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())
    hashed_password = self.hash_password(data['password'])

    #for item in data:
    lo_user = Usuario(primer_nombre=data['primer_nombre'], segundo_nombre=data['segundo_nombre'], 
                  primer_apellido=data['primer_apellido'], segundo_apellido=data['segundo_apellido'], active=data['active'],
                    superuser=data['superuser'], created=created, update=None, lastlogin=None, 
                    email=data['email'], password=hashed_password)
    lo_user.save()

    return { 'message': 'Usuario creado correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "userid" in data:
      lo_user = Usuario.query.get(data["userid"])
      if(lo_user is not None):
            # Actualizar solo si el dato es proporcionado
        if "primer_nombre" in data:
            lo_user.primer_nombre = data["primer_nombre"]
        if "segundo_nombre" in data:
            lo_user.segundo_nombre = data["segundo_nombre"]
        if "primer_apellido" in data:
            lo_user.primer_apellido = data["primer_apellido"]
        if "segundo_apellido" in data:
            lo_user.segundo_apellido = data["segundo_apellido"]
        if "email" in data:
            lo_user.email = data["email"]
        if "password" in data:
            lo_user.password = self.hash_password(data['password'])
        if "idrol" in data:
            lo_user.idrol = data["idrol"]
        if "idarea" in data:
            lo_user.idarea = data["idarea"]
        if "active" in data:
            lo_user.active = data["active"]
        if "superuser" in data:
            lo_user.superuser = data["superuser"]

        lo_user.update = int(time())
        
        lo_user.put()
        msg = {'message': 'Usuario actualizado correctamente.'}
      else:
        msg = {'error': 'No existe el usuario a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "userid" en payload enviado.'}, 404

    return msg
  
  def hash_password(self, password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()
  

class UserIDHandler(Resource):
  @jwt_required()
  def get(self, user_id=None):
    lo_user = Usuario.query.get(user_id)
    if(lo_user is not None):
      user_js = lo_user.serialize()
    else:
      user_js = {'error': 'No existe el usuario prueba'}, 404
    return user_js

class CurrentUserHandler(Resource):
  @jwt_required()
  def get(self):
    userid = get_jwt_identity()
    lo_user = Usuario.query.get(userid)
    if(lo_user is not None):
      user_js = lo_user.serialize()
    else:
      user_js = {'error': 'No existe el usuario logueado.'}, 404
    return user_js

class UserLogin(Resource):

  def post(self):

    data = request.get_json()
    email = data['email']
    password = data['password']

    users = Usuario.query.filter_by(email=email)

    isValid = False

    if(users.count() > 0):
      lo_user = users[0]

      isValid = self.verify_password(password, lo_user.password)

      if(isValid):
        expires = timedelta(minutes=60)
        access_token = create_access_token(identity=str(lo_user.userid), expires_delta=expires)
        lo_user.lastlogin = int(time())
        lo_user.put()
        rt_data = { 'access_token': access_token}
      else:
        rt_data = { 'message': "Contraseña incorrecta" }, 401

    else:
      rt_data = { 'message': "Usuario no existe" }, 401

    return rt_data
  
  def verify_password(self, password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
  