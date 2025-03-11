from flask import Flask, jsonify, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from os import getenv, environ

print("environ", environ)

app = Flask(__name__)

database_uri = getenv('DATABASE_URL')
print("database_uri", database_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = SQLAlchemy(app)


secret_key = getenv('SECRET_KEY')
jwt_secret_key = getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = secret_key
app.config["JWT_SECRET_KEY"] = jwt_secret_key
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

from app.routes import ROUTES, api_bp

api = Api(api_bp)

for resource, route in ROUTES:
  api.add_resource(resource, route)

app.register_blueprint(api_bp, url_prefix='/api')



