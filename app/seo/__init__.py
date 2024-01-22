from flask import Blueprint

seo = Blueprint('seo', __name__)

from . import routes
