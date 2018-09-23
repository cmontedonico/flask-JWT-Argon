from flask import Blueprint, Flask
from models import Session
from database import db_session
import jwt
import settings

app = Flask(__name__)
auth_token = Blueprint('auth_token', __name__)

def validate_auth(token):
    if token:
        try:    
            jwt_token = jwt.decode(token, settings.SECRET.get('key'), settings.SECRET.get('alg'))
            session = db_session.query(Session).filter(Session.user_id == jwt_token['user_id'], Session.token == token).first()
            if session:
                return session.user_id
            else:
                return False
        except Exception as e:
            return False
    else:
        return False
    return False
    