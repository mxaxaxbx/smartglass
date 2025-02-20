from app import db

class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  names = db.Column(db.String(120), nullable=False)
  surnames = db.Column(db.String(120), nullable=False)
  last_login = db.Column(db.Integer, nullable=False)
