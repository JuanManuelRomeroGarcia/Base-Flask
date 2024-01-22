from config import Config
from . import error
from app.models import db
from flask import current_app, redirect, render_template, request, url_for
from flask_babel import _


@error.app_errorhandler(404)
def not_found_error(error):
    url_not_found = request.path
    referrer = request.referrer or 'No referrer'
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Registro de advertencia con detalles del error
    current_app.logger.warning(
        f"404 list at URL: {url_not_found} - Referrer: {referrer} - List: {error} - IP: {ip_address} - User-Agent: {user_agent}"
    )

    return render_template('error/404.html', name='', mail_admin=Config.MAIL_ADMIN, url_not_found=url_not_found), 404

@error.app_errorhandler(405)
def method_not_allowed(error):
    requested_url = request.url  # URL que causó el error 405
    referrer = request.referrer or 'No referrer'
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    method_used = request.method  # Método HTTP que causó el error

    # Registro de advertencia con detalles del error
    current_app.logger.warning(
        f"405 Method Not Allowed at URL: {requested_url} - Referrer: {referrer} - Method: {method_used} - IP: {ip_address} - User-Agent: {user_agent}"
    )

    # Proporcionar una respuesta al usuario
    # Puedes personalizar la plantilla 'error/405.html' según tus necesidades
    return render_template('error/405.html', requested_url=requested_url, method_used=method_used, mail_admin=Config.MAIL_ADMIN), 405

@error.app_errorhandler(500)
def internal_error(error):
    # Registro detallado del error con la pila completa
    current_app.logger.exception('Internal Server Error: %s', str(error))
    db.session.rollback()
    return render_template('error/500.html', mail_admin=Config.MAIL_ADMIN), 500

@error.app_errorhandler(Exception)
def generic_error(error):
    # Registro detallado del error con información adicional
    current_app.logger.exception('Error: %s, URL: %s, Method: %s', str(error), request.url, request.method)
    db.session.rollback()
    return render_template('error/500.html', error_message=str(error), mail_admin=Config.MAIL_ADMIN), 500
