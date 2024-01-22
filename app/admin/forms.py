from wtforms import BooleanField, Form, StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, Optional
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l



class MyBaseForm(Form):
    pass

### Usuarios ### 

class RoleForm(FlaskForm):
    name = StringField(_l('Name Role'), validators=[DataRequired()])
    

class UserCreateForm(MyBaseForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    role = SelectField(_l('Role'),  validators=[InputRequired()])
    email_verified = BooleanField(_l('Email verified'))

class UserEditForm(MyBaseForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    role = SelectField(_l('Role'),validators=[InputRequired()])
    email_verified = BooleanField(_l('Email verified'))
