from flask import Blueprint

bp = Blueprint('main', __name__) # 'main': The name of the blueprint. Will be prepended to each endpoint name.

from app.main import routes # with this, registering a blueprint will also register its routes
