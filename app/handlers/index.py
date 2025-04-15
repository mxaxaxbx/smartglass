from flask_restful import Resource

from app.models.usuario import Usuario

class IndexHandler(Resource):

  def get(self):
    return { 'message': 'Welcome to smartglass' }
