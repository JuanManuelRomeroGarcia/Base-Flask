from flask import Blueprint

routers = Blueprint('routers', __name__, static_folder='static')


from . import routes
