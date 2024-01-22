from app.models.user import Role, User
from config import Config
from werkzeug.security import generate_password_hash
from . import db

# Crear la base de datos y los roles de usuario al iniciar la aplicación

def create_db():
    db.create_all()
    

        # Verificar si el rol 'admin' ya existe
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role is None:
        admin_role = Role(name='admin')
        db.session.add(admin_role)

    # Verificar si el rol 'user' ya existe
    user_role = Role.query.filter_by(name='user').first()
    if user_role is None:
        user_role = Role(name='user')
        db.session.add(user_role)

    # Hacer commit para guardar en la base de datos
    db.session.commit()

    # Verificar si el usuario 'admin' ya existe
    existing_admin_user = User.query.filter_by(username=Config.ADMIN).first()

    # Si el usuario 'admin' no existe, crearlo con el rol de admin y una contraseÃ±a segura
    if not existing_admin_user:
        # Generar una contraseña
        hashed_password = generate_password_hash(Config.ADMIN_PASSWORD)
        admin_user = User(username=Config.ADMIN, password=hashed_password)
        admin_user.roles.append(admin_role)  # Asignar el rol de admin al usuario
        admin_user.email = Config.MAIL_ADMIN
        admin_user.email_verified = True
        admin_user.email_verification_token = admin_user.get_email_verification_token()
        db.session.add(admin_user)

        # Hacer commit para guardar en la base de datos
    db.session.commit()