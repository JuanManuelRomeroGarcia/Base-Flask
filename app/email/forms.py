from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField, SubmitField, TextAreaField

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_babel import lazy_gettext as _l



class ResendVerificationEmailForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()],  render_kw={"placeholder": _l("Email")})
    submit = SubmitField(_l('Request verification Reset'),render_kw={'class': 'btn btn-dark'})
