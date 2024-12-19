from flask_restful import Resource

from app.models.user import User

class Index(Resource):

  def get(self):
    return { 'message': 'Welcome to smartglass' }
