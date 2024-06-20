from flask import jsonify, make_response, g
from app import auth
from app.api.models import User
import os


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


@auth.verify_password
def verify_password(username, password):
    if username == os.environ.get("CLI_ID") and password == os.environ.get("CLI_PWD"):  # admin auth
        return True
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):  # user auth
        return False
    g.user = user
    return True


@auth.get_password
def get_password(username):
    """
    In a more complex system this fun could check a user db
    """
    if username == os.environ.get("CLI_ID"):
        return os.environ.get("CLI_PWD")  # admin auth
    user = User.query.filter_by(username=username).first()
    if user:
        return user.pwd_hash  # user auth
    return None
