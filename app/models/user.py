from datetime import datetime, timedelta

from config import Config
from flask_babel import _
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from .utils import generate_jwt_token, temporary_email_domains


import re
import jwt
from app.models import db

from flask_login import UserMixin

class Role(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256))
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(256))
    
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    ### Validates ###
    @validates('email')
    def validate_email(self, key, email):
        # Validar formato del correo electrónico
        assert re.match("[^@]+@[^@]+\\.[^@]+", email)

        # Validar contra correos temporales
        domain = email.split('@')[1]
        if domain in temporary_email_domains:
            raise AssertionError(_('Temporary email not allowed'))

        return email

    @validates('username')
    def validate_username(self, key, username):
        if not re.match("^\\w+$", username):
            # Lanzar una excepción con un mensaje de error
            raise ValueError(_('Invalid username. Only alphanumeric characters and underscores are allowed.'))
        return username
    

    @staticmethod
    def verify_reset_password_token(token):      
        
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    ### Utils User ###

    
    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    

   
    def get_reset_password_token(self, expires_in=600):
        exp = datetime.now(Config.TIMEZONE) + timedelta(seconds=expires_in)
        payload = {'reset_password': self.id}
        return generate_jwt_token(payload, expiration_minutes=expires_in // 60)  # Convierte segundos a minutos
    
    def get_email_verification_token(self, expires_in=3600):
        payload = {'verify_email': self.id}
        return generate_jwt_token(payload, expiration_minutes=expires_in // 60)  # Convierte segundos a minutos