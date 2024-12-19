from flask_restful import Resource

from app.models.user import User

class Index(Resource):

  def get(self):
    users = User.query.all()
    return [user.email for user in users]
