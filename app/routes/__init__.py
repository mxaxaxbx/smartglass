from flask import Blueprint

from app.handlers.index import Index

ROUTES = [
  (Index, '/'),
]

api_bp = Blueprint('api', __name__)
