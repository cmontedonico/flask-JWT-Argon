from flask import Blueprint, Flask, request, jsonify
from flask_argon2 import Argon2
from models import User,Session
from database import db_session
import jwt
import settings
from datetime import datetime, timedelta

app = Flask(__name__)
argon2 = Argon2(app)
login_api = Blueprint('login_api', __name__)

@login_api.route("/try", methods = ['POST'])
def login():
    if request.json is None:
        return jsonify({"success": False, "error": "No data given"}), 404

    if 'username' in request.json:
        username = request.json['username']
    else:
        return jsonify({"success": False, "error": "No username given"}), 404

    if 'password' in request.json:
        password = request.json['password']
    else:
        return jsonify({"success": False, "error": "No password given"}), 404

    user = login_check(username, password)

    if user:
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=settings.SESSION.get('token_expiration'))
        }
        jwt_token = jwt.encode(payload, settings.SECRET.get('key'), settings.SECRET.get('alg'))
        ret_id = user.id
        #Save Token in Database session 
        if addSession(jwt_token, user.id):
            return jsonify({"success": True, "data":{'token': jwt_token.decode('UTF-8'), "id":ret_id} }), 200
        else:
            return jsonify({"success": False, "data": { "error": "User or Token Invalid"}}), 403
    else:
        return jsonify({"success": False, "data": { "error": "User or Token Invalid"}}), 403


@login_api.route("/signup", methods = ['POST'])
def signup():
    if request.json is None:
        return jsonify({"success": False, "error": "No data given"}), 404

    if 'username' in request.json:
        username = request.json['username']
    else:
        return jsonify({"success": False, "error": "No username given"}), 404

    if 'password' in request.json:
        password = request.json['password']
        pw_hash = argon2.generate_password_hash(password)
    else:
        return jsonify({"success": False, "error": "No password given"}), 404

    if 'email' in request.json:
        email = request.json['email']
    else:
        email = None

    if 'name' in request.json:
        name = request.json['name']
    else:
        name = None

    user = db_session.query(User).filter(User.username == username)

    if user.count() == 1:
        db_session.flush()
        return jsonify({"success": False, "error":"User already registered"}), 418
    else:
        try:
            newUser = User(username,pw_hash,email,name)
            db_session.add(newUser)
            db_session.flush()
            db_session.commit()
            return jsonify({"success": True, "data":{"id":newUser.id}}), 200
        except Exception as e:
            db_session.rollback()
            db_session.flush()
            print(e)
            return jsonify({"success": False, "error": "Error inserting user"}), 403
        finally:
            db_session.close()


def login_check(username=None, password=None):
    user = db_session.query(User).filter(User.username == username, User.status == 1)

    if user.count() == 1:
        pw_hash = user[0].password

        try:
            if Argon2().check_password_hash(pw_hash, password):
                return user[0]
            else:
                return False
        except Exception as e:
            return False
    else:
        return False

def addSession(token, user_id):
    user = db_session.query(User).filter(User.id == user_id, User.status == 1)
    if user.count() == 1:
        session = Session(user_id, token, '0.0.0.0', '{"browser": "chrome"}')
        try:
            db_session.add(session)
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            db_session.flush()
            return False
        finally:
            db_session.close()