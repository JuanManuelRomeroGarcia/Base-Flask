from functools import wraps
from flask_login import current_user
from flask_mail import Message
from app import mail

from flask import flash, redirect, render_template, url_for
from flask_babel import _


from config import Config


### emails ###

def send_email(subject, sender, recipients, template, **kwargs):
    html_content = render_template(template, **kwargs)
    html_body = render_template('email/email_base.html', content=html_content)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        _('Reset Your Password'),
        sender=("Base Flask", Config.MAIL_USERNAME),
        recipients=[user.email],
        template='email/especificas/reset_password.html',
        user=user,
        token=token
    )


def send_email_verification_email(user):
    send_email(
        _('Email Verification'),
        sender=("Base Flask", Config.MAIL_USERNAME),
        recipients=[user.email],
        template='email/especificas/verification.html',
        user=user,
        token=user.email_verification_token
    )



### Decoradores ###

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verifica si el usuario actual tiene uno de los roles permitidos
            if not current_user.is_authenticated or not any(role.name in allowed_roles for role in current_user.roles):
                flash(_('You do not have permission to access'), 'error')
                return redirect(url_for('auth.login'))  
            return f(*args, **kwargs)
        return decorated_function
    return decorator




