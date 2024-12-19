from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy 

from os import getenv, environ

print("environ", environ)

app = Flask(__name__)

database_uri = getenv('DATABASE_URL')
print("database_uri", database_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = SQLAlchemy(app)

from app.routes import ROUTES, api_bp

api = Api(api_bp)

for resource, route in ROUTES:
  api.add_resource(resource, route)

app.register_blueprint(api_bp, url_prefix='/api')

