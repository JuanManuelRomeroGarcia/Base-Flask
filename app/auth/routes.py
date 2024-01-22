
import re
from app.auth.forms import ChangePasswordForm, LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm

from app.models.user import Role, db, User
from app.email.utils import  send_email_verification_email, send_password_reset_email

from . import auth
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _



@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            

            if not user.email_verified:
                flash(_('Your email has not been verified. Please verify your email before login.'), 'warning')
                return redirect(url_for('auth.login'))
            

            login_user(user, remember=True)
            session['user_id'] = user.id 
            session.permanent = True

            flash(_('Welcome %(username)s', username=user.username), 'success')
        
        else:
            flash(_('Username or password incorrect'), 'error')
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', login_form=login_form, title=_('Login App'))
   


@auth.route('/logout',  methods=['GET', 'POST'])
@login_required
def logout():
    logout_user() 
    session.pop('user_id', None)
    flash(_('You have logged out, we hope to see you soon.'), 'success' )
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    user_role = Role.query.filter_by(name='user').first()

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if registration_form.validate_on_submit():
        # Validar el formato del nombre de usuario
        if not re.match(r"^\w+$", registration_form.username.data):
            registration_form.username.errors.append(_('Invalid username. Only alphanumeric characters and underscores are allowed.'))
            return render_template('auth/register.html', title=_('Register from App-Manuals'), registration_form=registration_form)
        

        existing_user_by_email = User.query.filter_by(email=registration_form.email.data).first()
        existing_user_by_username = User.query.filter_by(username=registration_form.username.data).first()

        if existing_user_by_username:
            registration_form.username.errors.append(_('The username is already taken. Please choose a different username.'))
        elif existing_user_by_email:
            registration_form.email.errors.append(_('The email is already registered. Please use another email.'))
        else:
            try:
                user = User(username=registration_form.username.data,
                            email=registration_form.email.data,
                        )

                user.set_password(registration_form.password.data)
                user.roles.append(user_role)
                user.email_verified = False
                user.email_verification_token = user.get_email_verification_token()
                db.session.add(user)
                db.session.commit()

                send_email_verification_email(user)

                flash(_('Congratulations, you are now a registered user!'), 'success')
                return redirect(url_for('auth.login'))

            except Exception as e:
                    registration_form.email.errors.append(str(e))
                    flash(_('An unexpected error occurred. Please try again.'), 'error')

    return render_template('auth/register.html', title=_('Register from App '), registration_form=registration_form)



@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    #print("Token recibido:", token)  
    user = User.verify_reset_password_token(token)
    if not user:
        #print("Token no válido")
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #print("Contraseña enviada:", form.password.data) 
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for instructions to reset your password'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)



@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            if form.new_password.data != form.confirm_new_password.data:
                flash(_('The new passwords do not match.'), 'danger')
            else:
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash(_('Your password has been successfully updated.'), 'success')
                return redirect(url_for('main.index'))
        else:
            flash(_('The current password is incorrect.'), 'danger')
    return render_template('auth/change_password.html', form=form)

