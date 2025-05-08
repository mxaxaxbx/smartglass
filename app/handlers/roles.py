from flask_restful import Resource, request

from app.models.rol import Rol
from time import time
from flask_jwt_extended import jwt_required, get_jwt_identity

class RolHandler(Resource):

  @jwt_required()
  def get(self):
    roles = Rol.query.all()
    rol_js = [rol.serialize() for rol in roles]
    return rol_js

  @jwt_required()
  def post(self):
    data = request.get_json()
    created = int(time())

    #for item in data:
    lo_rol = Rol(nombre=data['nombre'], endpoint=data['endpoint'], created=created, update=None)
    lo_rol.save()

    return { 'message': 'Rol Creado correctamente' }
  
  @jwt_required()
  def put(self):
    data = request.json  # Datos enviados en la solicitud
    msg = ""

    if "idrol" in data:
      lo_rol = Rol.query.get(data["idrol"])
      if(lo_rol is not None):
            # Actualizar solo si el dato es proporcionado
        if "nombre" in data:
            lo_rol.nombre = data["nombre"]
        if "endpoint" in data:
            lo_rol.endpoint = data["endpoint"]

        lo_rol.update = int(time())
        
        lo_rol.put()        
        msg = {'message': 'Rol actualizado correctamente.'}
      else:
        msg = {'error': 'No existe el rol a actualizar.'}, 404
    else:
      msg = {'error': 'No existe atributo "idrol" en payload enviado.'}, 404

    return msg
  
  
class RolIDHandler(Resource):
  @jwt_required()
  def get(self, idrol=None):
    rol2 = Rol.query.get(idrol)
    if(rol2 is not None):
      rol2 = rol2.serialize()
    else:
      rol2 = {'error': 'No existe el rol'}, 404
    return rol2

"""class CurrentUserHandler(Resource):
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
  """