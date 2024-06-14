from flask import abort, jsonify, request, url_for
from app import auth, db
from app.api import bp
from app.api.models import User
from app.api.errors import ERR_JSON, ERR_USERS_KEYSYNTAX, ERR_USERS_NAMELEN, ERR_USERS_NFIELD
import os


# UTILS
def make_public_user(user):
    """When GET request, sends back the whole path of the user_id"""
    new_user = {}
    for field in user:
        if field == 'joueur':
            new_user['uri'] = url_for('api.get_user', user_id=user['joueur'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


# ROUTES
@bp.route('/v1/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.all()
    users_list = [{'uri': url_for('api.get_user', user_id=user.id, _external=True), 'username': user.username, 'pwd': user.pwd} for user in users]
    return jsonify(users_list)


@bp.route('/v1/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user_data = {'id': user.id, 'username': user.username, 'pwd': user.pwd}
    return jsonify(user_data)


@bp.route('/v1/users', methods=['POST'])
@auth.login_required
def create_user():

    username = request.json['username']
    pwd = request.json['pwd']

    # ERROR HANDLING
    if not request.json:
        abort(400, description=ERR_JSON)
    if len(request.json) != 2:
        abort(400, description=ERR_USERS_NFIELD)
    if len(request.json) == 2 and not ('username' or 'pwd') in request.json:
        abort(400, description=ERR_USERS_KEYSYNTAX)
    if len(request.json['username']) < 2:
        abort(400, description=ERR_USERS_NAMELEN)
    # if User.query.filter_by(username=username).first() is not None:
    #     abort(400, description="User with this username already exists")
    # if not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", request.json['email']):
    #     abort(400, description=ERR_USERS_EMAILSYNTAX)

    # DB
    new_user = User(username=username, pwd=pwd)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id, 'username': new_user.username, 'pwd': new_user.pwd}), 201


# AUTH
@auth.get_password
def get_password(username):
    """
    In a more complex system this fun could check a user db
    TODO: DO NOT KEEP PWD HERE, add it in .env
    """
    if username == os.environ.get("CLI_ID"):
        return os.environ.get("CLI_PWD")
    return None
