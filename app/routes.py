from app import app, auth, users, logs
from flask import abort, jsonify, request, url_for
import re


# GLOBAL VARIABLES
ERR_JSON = "Not a json object"
ERR_USERS_NFIELD = "Users - Missing required fields (email, firstName, lastName)"
ERR_USERS_KEYSYNTAX = "Users - Incorrect key syntax (email, firstName, lastName)"
ERR_USERS_EMAILSYNTAX = "Users - Incorrect email syntax"
ERR_USERS_NAMELEN = "Users - firstName and lastName values must be at least 2 characters long"


# UTILS
def make_public_user(user):
    """When GET request, sends back the whole path of the user_id"""
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


def make_public_log(log):
    """When GET request, sends back the whole path of the log_id"""
    new_log = {}
    for field in log:
        if field == 'id':
            new_log['uri'] = url_for('get_log', log_id=log['id'], _external=True)
        else:
            new_log[field] = log[field]
    return new_log


# ROUTES
@app.route('/')
def index():
    return "Welcome to TSADK lol"


# users
@app.route('/tsadk/api/v1/users', methods=['GET'])
@auth.login_required
def get_users():
    return jsonify({'users': [make_public_user(user) for user in users]})


@app.route('/tsadk/api/v1/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@app.route('/tsadk/api/v1/users', methods=['POST'])
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
        'id': users[-1]['id'] + 1,
        'email': request.json['email'],
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
    }
    users.append(user)
    return jsonify({"user": user}), 201


# logs
@app.route('/tsadk/api/v1/logs', methods=['GET'])
@auth.login_required
def get_logs():
    return jsonify({'logs': [make_public_log(log) for log in logs]})


@app.route('/tsadk/api/v1/logs/<int:log_id>', methods=['GET'])
@auth.login_required
def get_log(log_id):
    log = [log for log in logs if log['id'] == log_id]
    if len(log) == 0:
        abort(404)
    return jsonify({'log': log[0]})


@app.route('/tsadk/api/v1/logs', methods=['POST'])
@auth.login_required
def create_log():
    if not request.json:
        abort(400, description=ERR_JSON)
    # TO SEE WITH MARIEM
    log = {
        'id': logs[-1]['id'] + 1,
        'timestamp': request.json['timestamp'],
        'nomSalle': request.json['nomSalle'],
        'action': request.json['action'],
    }
    logs.append(log)
    return jsonify({"log": log}), 201


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


if __name__ == '__main__':
    app.run(debug=True)
