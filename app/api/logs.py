from flask import abort, jsonify, request, url_for
from app import auth, db
from app.api import bp
from app.api.models import Log, User
from app.api.errors import ERR_JSON, ERR_LOGS_KEYSYNTAX, ERR_LOGS_NFIELD
import os
import sqlalchemy as sa


# UTILS
def make_public_log(log):
    """When GET request, sends back the whole path of the log_id"""
    new_log = {}
    for field in log:
        if field == 'id':
            new_log['uri'] = url_for('api.get_log', log_id=log['id'],
                                     _external=True)
        else:
            new_log[field] = log[field]
    return new_log


# ROUTES
@bp.route('/v1/logs', methods=['GET'])
@auth.login_required
def get_logs():
    return jsonify({'logs': [make_public_log(log) for log in logs]})


@bp.route('/v1/logs/<int:log_id>', methods=['GET'])
@auth.login_required
def get_log(log_id):
    if logs == 0:
        abort(404)
    log = [log for log in logs if log['id'] == log_id]
    if len(log) == 0:
        abort(404)
    return jsonify({'log': log[0]})


@bp.route('/v1/logs', methods=['POST'])
@auth.login_required
def create_log():
    if not request.json:
        abort(400, description=ERR_JSON)

    # TO SEE WITH MARIEM
    # if len(request.json) != 3:
    #     abort(400, description=ERR_LOGS_NFIELD)
    # if len(request.json) == 3 and not ('email' or 'firstName' or 'lastName') in request.json:
    #     abort(400, description=ERR_LOGS_KEYSYNTAX)
    id = logs[-1]['id'] + 1 if logs else 1

    # DB CHECK FOR USER
    query = sa.select(User)
    users = db.session.scalars(query)
    for u in users:
        if u.id == request.json["id"]:
            print("we are talking about", u.id, u.username)
        # logPush = Log(id=id,
        #               action=request.json['action'])
        # db.session.add(logPush)
        # db.session.commit()

    # DB PUSH

    # JSON
    log = {
        'id': id,
        'userID': request.json['userID'],
        'timestamp': request.json['timestamp'],
        # 'sequence': request.json['sequence'],
        # 'roomName': request.json['roomName'],
        # 'actionNature': request.json['actionNature'],
        # 'actionType': request.json['actionType'],
        # 'userAnswer': request.json['userAnswer'],
        # 'userError': request.json['userError'],
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
    if username == os.environ.get("CLI_ID"):
        return os.environ.get("CLI_PWD")
    return None
