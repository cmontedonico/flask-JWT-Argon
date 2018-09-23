from flask import Flask, jsonify
from database import Base, db_session, init_db
from controllers.login_api import login_api
from controllers.user_api import user_api

app = Flask(__name__)
app.register_blueprint(login_api, url_prefix="/api/v1/login")
app.register_blueprint(user_api, url_prefix="/api/v1/user")

@app.route("/")
def hello():
    return jsonify({"Everything is Awesome": "Everything is cool when you are part of a team"})

#initializamos la Base
@app.route("/database")
def db_init():
    init_db()
    return "Listo"

@app.after_request
def call_after_request_callbacks(response):
    try:
        db_session.remove()
    except Exception as e:
        print(e)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)