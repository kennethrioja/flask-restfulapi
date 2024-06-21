from flask import jsonify, make_response, g
from app.api.models import User
from app import auth
from functools import wraps


def check_access(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(username=auth.current_user()).first()
            if user and user.role in allowed_roles:
                return f(*args, **kwargs)
            else:
                return jsonify({"message": "Access forbidden"}), 403
        return decorated_function
    return decorator
