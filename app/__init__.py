from flask import Flask, has_request_context, session
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_talisman import GOOGLE_CSP_POLICY, Talisman
from app.csp import csp
from app.error.utils import configure_logging

from app.models.create_db import create_db
from config import Config
from flask_babel import Babel, _
from .models import db


def get_locale():
    if not has_request_context():
        return Config.BABEL_DEFAULT_LOCALE
    return session.get('language', Config.BABEL_DEFAULT_LOCALE)

mail = Mail()
bootstrap = Bootstrap5()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
     
    merged_csp = dict(GOOGLE_CSP_POLICY, **csp)
    Talisman(app,
            content_security_policy=merged_csp,
            content_security_policy_nonce_in=['script-src', 'style-src', 'frame-src']
            )

    # Configuración del logging
    configure_logging(app, config_class)

    db.init_app(app)
    with app.app_context():
        create_db() 

    login_manager.init_app(app)
    
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app,  locale_selector=get_locale)
   
    from .admin import admin_app
    admin_app.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth' )

    from .email import email as email_blueprint
    app.register_blueprint(email_blueprint, url_prefix='/email' )

    from .error import error as error_blueprint
    app.register_blueprint(error_blueprint, url_prefix='/error' )

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .seo import seo as seo_blueprint
    app.register_blueprint(seo_blueprint, url_prefix='/')

    # Repite para otros blueprints

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))