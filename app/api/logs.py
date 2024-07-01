from flask import abort, jsonify, request, url_for
from app import auth, db
from app.api import bp
from app.api.models import Log, User
from app.api.errors import ERR_JSON, ERR_LOGS_KEYSYNTAX, ERR_LOGS_NFIELD, \
    ERR_LOGS_NOUSERSFOUND, ERR_LOGS_INVALIDUSERID
from .auth.decorators import check_access
from sqlalchemy.inspection import inspect
import os


# UTILS
def make_public_log(log):
    """When GET request, sends back the whole path of the log_id"""
    new_log = {}
    for field in log:
        if field == "id":
            new_log["uri"] = url_for("api.get_log", log_id=log["id"],
                                     _external=True)
        else:
            new_log[field] = log[field]
    return new_log


# ROUTES
@bp.route("/v1/logs", methods=["GET"])
@auth.login_required
@check_access(allowed_roles=["admin"])
def get_logs():
    logs = Log.query.all()

    if logs is None:
        abort(404)

    logs_list = []
    for log in logs:
        log_dict = {"uri": url_for("api.get_log", log_id=log.id,
                                   _external=True)}
        for column in inspect(Log).c:
            log_dict[column.name] = getattr(log, column.name)
        logs_list.append(log_dict)
    return jsonify(logs_list)


@bp.route("/v1/logs/<int:log_id>", methods=["GET"])
@auth.login_required
@check_access(allowed_roles=["admin"])
def get_log(log_id):
    log = Log.query.get(log_id)

    if log is None:
        abort(404)

    log_data = {}
    for column in inspect(Log).c:
        log_data[column.name] = getattr(log, column.name)
    return jsonify({log_data})


@bp.route("/v1/logs", methods=["POST"])
@auth.login_required
@check_access(allowed_roles=["admin"])
# def create_log():
#     userID = request.json["userID"]
#     user = User.query.get(userID)
#     timestamp = request.json["timestamp"]

#     if user is None:  # no users found
#         abort(400, description=ERR_LOGS_NOUSERSFOUND)
#     if auth.current_user() != os.environ.get("CLI_ID"):
#         usertoken = User.verify_auth_token(auth.current_user())
#         if user.id != usertoken.id:  # check token.id if it is the same than userID
#             abort(400, description=ERR_LOGS_INVALIDUSERID)
#     if not request.json:
#         abort(400, description=ERR_JSON)
#     if len(request.json) != 2:
#         abort(400, description=ERR_LOGS_NFIELD)
#     if len(request.json) == 2 and not ("userID" or "timestamp") in request.json:
#         abort(400, description=ERR_LOGS_KEYSYNTAX)

#     new_log = Log(userID=userID, timestamp=timestamp)
#     db.session.add(new_log)
#     db.session.commit()
#     return jsonify({"id": new_log.id, "userID": new_log.userID, "timestamp": new_log.timestamp})
def create_log():
    if not request.json:
        abort(400, description=ERR_JSON)

    log_data = {}
    for field in Log.__table__.columns.keys():
        if field == "id":
            continue
        if field in request.json:
            log_data[field] = request.json[field]
        else:
            abort(400, description=f"Missing field '{field}' in request.")

    user = User.query.get(log_data["userID"])
    if user is None:
        abort(400, description=ERR_LOGS_NOUSERSFOUND)

    if auth.current_user() != os.environ.get("CLI_ID"):
        usertoken = User.verify_auth_token(auth.current_user())
        if usertoken.id != log_data["userID"]:
            abort(400, description=ERR_LOGS_INVALIDUSERID)

    new_log = Log(**log_data)
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"id": new_log.id, **log_data})
