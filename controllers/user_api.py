from flask import Flask, Blueprint, jsonify, request
from models import User
from controllers.auth_token import validate_auth
from database import db_session

app = Flask(__name__)
user_api = Blueprint('user_api', __name__)


@user_api.route("/profile", methods = ['GET'])
def profile():
    user_id = validate_auth(request.headers.get('Authorization'))
    if not user_id:
        return jsonify({"success": False, "error": "Invalid Authorization"}), 418

    user = db_session.query(User).filter(User.id == user_id)

    if user.count() == 1:
        return jsonify({
            "success": True,
                        "data": {
                            "id":user_id,
                            "name": user[0].name,
                            "email": user[0].email,
                            "username": user[0].username,
                            "since": user[0].created_at
                        }
            }
        ), 200
    else:
        return jsonify({"success": False, "error": "User not found"}), 418


