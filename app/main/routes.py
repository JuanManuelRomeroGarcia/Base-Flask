from flask import flash, redirect, render_template, request, session, url_for
from flask_babel import _
from app.email.utils import role_required
from config import Config
from . import main 

@main.route('/')
def index():
    return render_template('index.html', title=_("Home"))


@main.route('/localizar')
@role_required(['user'])
def localizar():
    return 'Prueba de role required'



@main.route('/set_language', methods=['POST'])
def set_language():
    lang = request.form.get('language')
    if lang in Config.LANGUAGES:
        session['language'] = lang
        flash(_('Language changed successfully.'),'success')
        return redirect(request.referrer or url_for('admin.index'))
    else:
        flash(_('Invalid language selection.'),'error')
    return redirect(request.referrer or url_for('admin.index'))