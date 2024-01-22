from datetime import datetime
from flask import flash, redirect, render_template, request, url_for

from app.email.forms import ResendVerificationEmailForm
from app.email.utils import send_email_verification_email
from app.models.user import db, User
from flask_babel import _
from . import email


@email.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(email_verification_token=token).first()
    if user:
        user.email_verified = True
        user.active = True
        user.confirmed_at = datetime.utcnow()
        db.session.commit()
        flash(_('Your email has been successfully verified! Now you can log in.'), 'success')
        return redirect(url_for('auth.login'))
    else:
        flash(_('Invalid verification token. Please request verification again.'), 'error')
        return redirect(url_for('main.index'))
    
    
@email.route('/resend_verification_email', methods=['GET', 'POST'])
def resend_verification_email():
    form = ResendVerificationEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.email_verified:
            user.email_verification_token = user.get_reset_password_token()
            user.active = True
            user.confirmed_at = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            send_email_verification_email(user)  # Llamada a la función para enviar el correo de confirmación
            flash(_('New confirmation email was sent. Please verify your email.'), 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(_('A new confirmation email cannot be sent. Your email is now verified.'), 'error')

    return render_template('email/resend_verification_email.html', form=form, title="Reenviar Confirmación Email")





