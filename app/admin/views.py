
from flask import flash, redirect, request, url_for
from flask_login import current_user
from flask_admin import AdminIndexView

from flask_admin.form import rules
from flask_admin.contrib.sqla import ModelView


from app.admin.forms import RoleForm, UserCreateForm, UserEditForm
from flask_babel import _, lazy_gettext as _l

from app.models.user import Role


class AdminAuthenticationMixin:
    def is_accessible(self):
        # Verifica si el usuario está autenticado y tiene el rol "admin"
        return current_user.is_authenticated and any(role.name in ['admin'] for role in current_user.roles)

    def inaccessible_callback(self, name, **kwargs):
        # Redirige al usuario a la página de inicio de sesión si no cumple con los requisitos
        flash(_l('You have to be admin'), 'error')
        return redirect(url_for('admin.index', next=request.url))


class MyAdminIndexView(AdminIndexView):
    '''Vista principal'''
    def is_accessible(self):
        # Verifica si el usuario está autenticado y tiene el rol "admin"
        return current_user.is_authenticated and any(role.name in ['admin'] for role in current_user.roles)


    def inaccessible_callback(self, name, **kwargs):
        # Redirige al usuario a la página de inicio de sesión si no cumple con los requisitos
        return redirect(url_for('auth.login', next=request.url))

class RoleView(AdminAuthenticationMixin, ModelView):

    
    def create_model(self, form):
    # Verifica si el usuario tiene el rol "super_admin" para crear
        if current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles):
            return super(RoleView, self).create_model(form)
        
        else:
            flash(_l('You do not have permission to create users'), 'error')
            return False

    def update_model(self, form, model):
        # Verifica si el usuario tiene el rol "super_admin" para editar
        if current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles):
            return super(RoleView, self).update_model(form, model)
        else:
            flash(_l('You do not have permission to edit users'), 'error')
            return False
    
    def delete_model(self, model):
        # Verifica si el usuario tiene el rol "super_admin" para editar
        if current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles):
            return super(RoleView, self).delete_model(model)
        else:
            flash(_l('You do not have permission to edit users'), 'error')
            return False

    
    can_create = True  # No permitir la creación de nuevos registros
    can_edit = True     # Permitir la edición de registros existentes
    can_delete = True   # Permitir la eliminación de registros existentes
    can_export= True    # Permitir la exportacion del archivo
    can_view_details = False
    page_size = 15 # Numero de lineas

    column_labels = {
        'name': _l('Name'),
        'description': _l('Description'),
    }

    form = RoleForm 

    form_create_rules = [
        rules.Field(_('name')),
    ]



class UserView(AdminAuthenticationMixin, ModelView):

    def _user_role(view, context, model, name):
        if model.roles:
            return ', '.join(role.name for role in model.roles)
        return 'Sin Rol'
        
    def create_model(self, form):
        # Verifica si el usuario tiene el rol "super_admin" para crear
        if current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles):
            return super(UserView, self).create_model(form)
        else:
            flash(_l('You do not have permission to create users'), 'error')
            return False

    def update_model(self, form, model):
        # Verifica si el usuario tiene el rol "super_admin" para editar
        if current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles):
            return super(UserView, self).update_model(form, model)
        else:
            flash(_l('You do not have permission to edit users'), 'error')
            return False
        
    def delete_model(self, model):
        # Verifica si el usuario tiene el rol "super_admin" para editar
        if current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles):
            return super(UserView, self).delete_model(model)
        else:
            flash(_l('You do not have permission to edit users'), 'error')
            return False
            

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = False
    page_size = 15 # Numero de lineas

    column_exclude_list = ['password', 'email_verification_token']
    column_list = ['username', 'email', 'role','email_verified']
    column_formatters = {
    'role': _user_role
    }

    column_labels = {
        'username': _l('Username'),
        'role': _l('Role'),
        'email': _l('Email'),
        'password': _l('Password'),
        'email_verified': _l('Email verified'),

        
    }

    form = UserCreateForm
    edit_form = UserEditForm

    form_create_rules = [
        rules.Field(_('username')),
        rules.Field(_('password')),
        rules.Field(_('email')), 
        rules.Field(_('role')),
        rules.Field(_('email_verified')),
        
    ]
       

    def on_model_change(self, form, model, is_created):
        if is_created:
            
            model.email_verification_token = model.get_email_verification_token()
            model.email_verified = form.email_verified.data
            model.email = form.email.data

            if form.password.data:
                model.set_password(form.password.data) 
           

            role_name = form.role.data
        
            role = Role.query.filter_by(name=role_name).first()

            if role:
                model.roles.append(role)
         
        else:
            
            # Actualiza los campos básicos
            model.email = form.email.data
                
            # Procesar cambio de rol
            role_name = form.role.data
            role = Role.query.filter_by(name=role_name).first()
            if role:
                model.roles[:] = [role]
            else:
                flash(f"Rol '{role_name}' no encontrado.", 'error')
                return False


    def edit_form(self, obj=None):
        form = super(UserView, self).edit_form(obj)
        del form.password
        form.role.choices = [(role.name, role.name) for role in Role.query.all()]
        if obj and obj.roles and not form.role.data:
            form.role.data = obj.roles[0].name
        return form

