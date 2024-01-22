
## JWT ##

from datetime import datetime, timedelta
import jwt
from config import Config


# Define la función para generar tokens JWT
def generate_jwt_token(payload, expiration_minutes=60):
    """
    Genera un token JWT con un payload y tiempo de expiración personalizables.

    Args:
        payload (dict): El payload que deseas incluir en el token.
        expiration_minutes (int): El tiempo de expiración del token en minutos. Predeterminado: 60 minutos.

    Returns:
        str: El token JWT generado.
    """
    # Calcula la fecha de expiración
    expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    # Agrega la fecha de expiración al payload
    payload['exp'] = expiration

    # Genera el token JWT utilizando la clave secreta
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    return token

## Correos Temporales ##


temporary_email_domains = [
    "10minutemail.com",
    "tempmail.com",
    "temp-mail.org",
    "mailinator.com",
    "yopmail.com",
    "guerrillamail.com",
    "throwawaymail.com",
    "dispostable.com",
    "maildrop.cc",
    "getnada.com",
    "trashmail.com",
    "temp-mail.org",
    "spambog.com",
    "harakirimail.com",
    "fakeinbox.com",
    "sneakemail.com",
    "mailnesia.com",
    "mytrashmail.com",
    "spamgourmet.com",
    "gmial.com",
    "0mail.com",
    "gufum.com",  
    "vasteron.com",
    "talmetry.com",
    "cazlv.com",
    "cwmxc.com",
]
