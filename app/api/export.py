from app import auth
from app.api import bp
from app.api.models import Log
import csv
from io import StringIO
from flask import make_response
from datetime import date


@bp.route('/v1/export/logs', methods=['GET'])
@auth.login_required
def export_logs():
    si = StringIO()
    cw = csv.writer(si)
    records = Log.query.all()   # or a filtered set, of course
    # any table method that extracts an iterable will work
    cw.writerows([["id", "userID", "timestamp"]])
    cw.writerows([(r.id, r.userID, r.timestamp) for r in records])
    response = make_response(si.getvalue())
    today = str(date.today()).replace('-', '')
    response.headers['Content-Disposition'] = f'attachment; filename=tsadk_export_logs_{today}.csv'
    response.headers["Content-type"] = "text/csv"
    return response
