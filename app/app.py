#!flask/bin/python
from flask import Flask, abort, jsonify, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import re

# GLOBAL VARIABLES
ERR_JSON = "Not a json object"
ERR_USERS_NFIELD = "Users - Missing required fields (email, firstName, lastName)"
ERR_USERS_KEYSYNTAX = "Users - Incorrect key syntax (email, firstName, lastName)"
ERR_USERS_EMAILSYNTAX = "Users - Incorrect email syntax"
ERR_USERS_NAMELEN = "Users - firstName and lastName values must be at least 2 characters long"


app = Flask(__name__)
auth = HTTPBasicAuth()
users = [
    {
        "id": 1,
        "email": "first@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "logs": [
            {
                "id": 0,
                "timestamp": "17-05-2024 10:17:00",
                "nomSalle": "Doria",
                "action": "Walk",
            }
        ],
    }
]
logs = [
    {
        "id": 1,
        "timestamp": "17-05-2024 10:17:00",
        "nomSalle": "Mandur",
        "action": "Run",
    }
]


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
    return "Hello, World!"


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
@app.route('/tsadk/api/v1/users/<int:user_id>/logs', methods=['GET'])
@auth.login_required
def get_logs(user_id):
    user = [user for user in users if user['id'] == user_id]
    logs = user[0].get("logs")
    if len(user) == 0 or len(logs) == 0:
        abort(404)
    logs = user[0].get("logs")
    # if len(logs) == 0:
    #     abort(404)
    return jsonify({'logs': [make_public_log(user, log) for log in logs]})


@app.route('/tsadk/api/v1/users/<int:user_id>/logs/<int:log_id>', methods=['GET'])
@auth.login_required
def get_log(user_id, log_id):
    user = [user for user in users if user['id'] == user_id]
    logs = user[0].get("logs")
    log = [log for log in logs if log['id'] == log_id]
    if len(user) == 0 or len(logs) == 0 or len(log) == 0:
        abort(404)
    return jsonify({'log': log[0]})


@app.route('/tsadk/api/v1/users/<int:user_id>/logs', methods=['POST'])
@auth.login_required
def create_log(user_id):
    user = [user for user in users if user['id'] == user_id]
    logs = user[0].get("logs")
    if len(user) == 0 or len(logs) == 0:
        abort(404)
    if not request.json:
        abort(400, description=ERR_JSON)
    # if len(request.json) != 3:
    #     abort(400, description=ERR_USERS_NFIELD)
    # if len(request.json) == 3 and not ('email' or 'firstName' or 'lastName') in request.json:
    #     abort(400, description=ERR_USERS_KEYSYNTAX)
    # if not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", request.json['email']):
    #     abort(400, description=ERR_USERS_EMAILSYNTAX)
    # if len(request.json['firstName']) < 2 or len(request.json['lastName']) < 2:
    #     abort(400, description=ERR_USERS_NAMELEN)
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


# ERROR HANDLING
@app.errorhandler(400)
def bad_request(e):
    if e:
        return make_response(jsonify({"error": "Bad Request: " + e.description}), 400)
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not Found"}), 404)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


if __name__ == '__main__':
    app.run(debug=True)
