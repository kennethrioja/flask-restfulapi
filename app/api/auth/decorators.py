from flask import jsonify
from app.api.models import User
from app import auth
from functools import wraps
import os


def check_access(allowed_roles):
    """
    A decorator to check access permissions for routes based on user roles and
    authentication methods.

    Args:
        allowed_roles (list): A list of roles allowed to access the decorated
        route.

    Returns:
        function: The wrapped function if access is permitted, otherwise
        returns a 403 Forbidden response.

    The decorator checks for three types of authentication in the following
    order:
    1. Admin Authentication: Grants access if the current user matches the
       CLI_ID environment variable.
    2. Token Authentication: Verifies the user's token and grants access if
       valid.
    3. Role-Based Access Control: Grants access if the user's role is in the
       allowed_roles list.

    Example usage:
        @app.route('/some_protected_route')
        @check_access(['admin', 'user'])
        def some_protected_route():
            return jsonify({"message": "This is a protected route."})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if auth.current_user() == os.environ.get("CLI_ID"):  # admin auth
                return f(*args, **kwargs)
            user = User.verify_auth_token(auth.current_user())  # token auth
            if user:
                return f(*args, **kwargs)
            user = User.query.filter_by(username=auth.current_user()).first()
            if user and user.role in allowed_roles:  # role-based ac
                return f(*args, **kwargs)
            else:
                return jsonify({"message": "Access forbidden"}), 403
        return decorated_function
    return decorator
