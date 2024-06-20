from flask import jsonify, make_response
from app.api.errors import bp


# APP
@bp.app_errorhandler(400)
def bad_request(e):
    if e:
        return make_response(jsonify({"error": "Bad Request: " + e.description}), 400)
    return make_response(jsonify({"error": "Bad Request"}), 400)


@bp.app_errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not Found"}), 404)
