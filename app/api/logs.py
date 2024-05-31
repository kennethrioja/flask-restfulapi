from flask import abort, jsonify, request, url_for
from app import auth, logs
from app.api import bp
from app import ERR_JSON


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
