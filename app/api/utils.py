from flask import make_response, jsonify, g
from app import auth
from app.api import bp
from app.api.models import Log
from io import StringIO
from datetime import date
from .auth.decorators import check_access
from config import Config
import csv


@bp.route("/v1/utils/export/logs", methods=["GET"])
@auth.login_required
@check_access(allowed_roles=["admin"])
def export_logs():
    si = StringIO()
    cw = csv.writer(si)
    column_names = [column.name for column in Log.__table__.columns]
    cw.writerow(column_names)
    records = Log.query.all()
    for record in records:
        cw.writerow([getattr(record, column) for column in column_names])
    response = make_response(si.getvalue())
    today = str(date.today()).replace('-', '')
    response.headers["Content-type"] = "text/csv"
    response.headers["Content-Disposition"] = f"attachment;\
        filename={Config.APP_NAME}_export_logs_{today}.csv"
    return response


@bp.route("/v1/utils/token", methods=["GET"])
@auth.login_required
@check_access(allowed_roles=["admin", "user"])
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})
