from flask import abort, jsonify, request, url_for
from app import auth, db
from app.api import bp
from app.api.models import Log, User
from app.api.errors import ERR_JSON, ERR_LOGS_KEYSYNTAX, ERR_LOGS_NFIELD, ERR_LOGS_INVALIDUSERID


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
def get_logs():
    logs = Log.query.all()
    logs_list = [{"uri": url_for("api.get_log", log_id=log.id, _external=True), "userID": log.userID, "timestamp": log.timestamp} for log in logs]
    return jsonify(logs_list)


@bp.route("/v1/logs/<int:log_id>", methods=["GET"])
@auth.login_required
def get_log(log_id):
    log = Log.query.get(log_id)
    if log is None:
        abort(404)
    return jsonify({"id": log.id, "userID": log.userID, "timestamp": log.timestamp})


@bp.route("/v1/logs", methods=["POST"])
@auth.login_required
def create_log():

    userID = request.json["userID"]
    user = User.query.get(userID)
    if user is None:
        abort(400, description=ERR_LOGS_INVALIDUSERID)

    timestamp = request.json["timestamp"]

    # ERROR HANDLING
    if not request.json:
        abort(400, description=ERR_JSON)
    if len(request.json) != 2:
        abort(400, description=ERR_LOGS_NFIELD)
    if len(request.json) == 2 and not ("userID" or "timestamp") in request.json:
        abort(400, description=ERR_LOGS_KEYSYNTAX)

    # DB
    new_log = Log(userID=userID, timestamp=timestamp)
    db.session.add(new_log)
    db.session.commit()

    return jsonify({"id": new_log.id, "userID": new_log.userID, "timestamp": new_log.timestamp})
