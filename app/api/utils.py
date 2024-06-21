from flask import make_response, jsonify, g
from app import auth
from app.api import bp
from app.api.models import Log
from io import StringIO
from datetime import date
from .auth.decorators import check_access
import csv


@bp.route("/v1/utils/export/logs", methods=["GET"])
@auth.login_required
@check_access(allowed_roles=["admin"])
def export_logs():
    si = StringIO()
    cw = csv.writer(si)
    records = Log.query.all()   # or a filtered set, of course
    # any table method that extracts an iterable will work
    cw.writerows([["id", "userID", "timestamp"]])
    cw.writerows([(r.id, r.userID, r.timestamp) for r in records])
    response = make_response(si.getvalue())
    today = str(date.today()).replace('-', '')
    response.headers["Content-Disposition"] = f"attachment; filename=tsadk_export_logs_{today}.csv"
    response.headers["Content-type"] = "text/csv"
    return response


@bp.route("/v1/utils/token", methods=["GET"])
@auth.login_required
@check_access(allowed_roles=["admin", "user"])
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})
