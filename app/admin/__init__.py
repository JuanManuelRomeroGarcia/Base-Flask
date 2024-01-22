
from flask import flash
from flask_admin import Admin
from app import db
from flask_babel import _, lazy_gettext as _l
from app.models.user import Role, User
from .views import  MyAdminIndexView, RoleView, UserView

import warnings



admin_app = Admin(
    index_view=MyAdminIndexView(name=_l('Control Panel')),
    template_mode='bootstrap5', static_url_path='/static/',
)
admin_app.name = 'Base Flask Admin'


with warnings.catch_warnings(record=True) as captured_warnings:
    warnings.simplefilter("always")

    # Tu código para añadir vistas
    admin_app.add_view(RoleView(Role, db.session, name=_l('Role'), category=_l('User')))
    admin_app.add_view(UserView(User, db.session, name=_l('User'), category=_l('User')))

    # Imprimir las advertencias capturadas
    for warning in captured_warnings:
        flash(f"Advertencia: {warning.message}")