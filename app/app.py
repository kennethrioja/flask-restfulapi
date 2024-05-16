#!flask/bin/python
from flask import Flask, abort, jsonify, make_response, request, url_for
import re

ERR_JSON = "Not a json object"
ERR_NFIELDS = "Missing required fields (email, firstName, lastName)"
ERR_KEYSYNTAX = "Incorrect key syntax (email, firstName, lastName)"
ERR_EMAILSYNTAX = "Incorrect email syntax"
ERR_LEN = "firstName and lastName values must be at least 2 characters long"
app = Flask(__name__)
users = [
    {
        "id": 1,
        "email": "first@example.com",
        "firstName": "John",
        "lastName": "Doe"
    }
]


def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/tsadk/api/v1/users', methods=['GET'])
def get_users():
    return jsonify({'users': [make_public_user(user) for user in users]})


@app.route('/tsadk/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@app.route('/tsadk/api/v1/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400, description=ERR_JSON)
    if len(request.json) != 3:
        abort(400, description=ERR_NFIELDS)
    if len(request.json) == 3 and not ('email' or 'firstName' or 'lastName') in request.json:
        abort(400, description=ERR_KEYSYNTAX)
    if not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", request.json['email']):
        abort(400, description=ERR_EMAILSYNTAX)
    if len(request.json['firstName']) < 2 or len(request.json['lastName']) < 2:
        abort(400, description=ERR_LEN)
    user = {
        'id': users[-1]['id'] + 1,
        'email': request.json['email'],
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
    }
    users.append(user)
    return jsonify({"user": user}), 201


@app.errorhandler(400)
def bad_request(e):
    if e:
        return make_response(jsonify({"error": "Bad Request: " + e.description}), 400)
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not Found"}), 404)


if __name__ == '__main__':
    app.run(debug=True)
