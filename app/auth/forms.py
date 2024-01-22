from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _l




class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": _l('Username')})
    email = StringField(_l('Email'), validators=[DataRequired(), Email()],  render_kw={"placeholder": _l("Email")})
    password = PasswordField(_l('Password'), validators=[DataRequired(), EqualTo('confirm_password')],
                               render_kw={"placeholder": _l("Password")})
    confirm_password = PasswordField(_l('Confirm Password'), validators=[DataRequired()],
                                     render_kw={"placeholder": _l("Confirm password")})
    
    submit = SubmitField(_l('Register'), render_kw={'class': 'btn navbar-brand'})


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": _l('username')})
    password = PasswordField(_l('Password'), validators=[DataRequired()],  render_kw={"placeholder": _l("password")})
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Login'),render_kw={'class': 'btn navbar-brand'},)


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'),render_kw={'class': 'btn navbar-brand'})


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'),render_kw={'class': 'btn navbar-brand'})

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(_l('Current Password'), validators=[DataRequired()])
    new_password = PasswordField(_l('New Password'), validators=[DataRequired(), EqualTo('confirm_new_password', message=_l('Passwords must match'))])
    confirm_new_password = PasswordField(_l('Confirm New Password'), validators=[DataRequired()])
    submit_password = SubmitField(_l('Change Password'))


