from flask import abort, jsonify, request, url_for
from app import auth, users, logs
from app.api import bp
from app import ERR_JSON, ERR_USERS_EMAILSYNTAX, ERR_USERS_KEYSYNTAX, ERR_USERS_NAMELEN, ERR_USERS_NFIELD
import re


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
    return jsonify({'users': [make_public_user(user) for user in users]})


@bp.route('/v1/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = [user for user in users if user['joueur'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@bp.route('/v1/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json:
        abort(400, description=ERR_JSON)
    if len(request.json) != 3:
        abort(400, description=ERR_USERS_NFIELD)
    if len(request.json) == 3 and not ('email' or 'firstName' or 'lastName') in request.json:
        abort(400, description=ERR_USERS_KEYSYNTAX)
    if not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", request.json['email']):
        abort(400, description=ERR_USERS_EMAILSYNTAX)
    if len(request.json['firstName']) < 2 or len(request.json['lastName']) < 2:
        abort(400, description=ERR_USERS_NAMELEN)
    user = {
        'joueur': users[-1]['joueur'] + 1,
        'email': request.json['email'],
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
    }
    users.append(user)
    return jsonify({"user": user}), 201


# AUTH
@auth.get_password
def get_password(username):
    """
    In a more complex system this fun could check a user db
    TODO: DO NOT KEEP PWD HERE, add it in .env
    """
    if username == 'user1':
        return 'pwd1'
    return None
