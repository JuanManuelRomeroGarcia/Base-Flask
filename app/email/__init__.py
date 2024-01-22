from flask import Blueprint

email = Blueprint('email', __name__)

from . import routes
