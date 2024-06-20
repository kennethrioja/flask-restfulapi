from flask import abort, jsonify, request, url_for
from app import auth, db
from app.api import bp
from app.api.models import User
from app.api.errors import ERR_JSON, ERR_USERS_DUPLICATE, ERR_USERS_KEYSYNTAX, ERR_USERS_NAMELEN, ERR_USERS_NFIELD


# UTILS
def make_public_user(user):
    """When GET request, sends back the whole path of the user_id"""
    new_user = {}
    for field in user:
        if field == "joueur":
            new_user["uri"] = url_for("api.get_user", user_id=user["username"], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


# ROUTES
@bp.route("/v1/users", methods=["GET"])
@auth.login_required
def get_users():
    users = User.query.all()
    users_list = [{"uri": url_for("api.get_user", user_id=user.id, _external=True), "username": user.username} for user in users]
    return jsonify(users_list)


@bp.route("/v1/users/<int:user_id>", methods=["GET"])
@auth.login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user_data = {"id": user.id, "username": user.username}
    return jsonify(user_data)


@bp.route("/v1/users", methods=["POST"])
@auth.login_required
def create_user():

    username = request.json["username"]
    pwd = request.json["pwd"]

    # ERROR HANDLING
    if username is None or pwd is None:
        abort(400, description=ERR_JSON)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400, description=ERR_USERS_DUPLICATE)  # existing user
    if len(request.json["username"]) < 2:
        abort(400, description=ERR_USERS_NAMELEN)  # username len too short
    if len(request.json) != 2:
        abort(400, description=ERR_USERS_NFIELD)  # not sure to keep
    if len(request.json) == 2 and not ("username" or "pwd") in request.json:
        abort(400, description=ERR_USERS_KEYSYNTAX)  # not sure to keep
    # if User.query.filter_by(username=username).first() is not None:
    #     abort(400, description="User with this username already exists")
    # if not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", request.json["email"]):
    #     abort(400, description=ERR_USERS_EMAILSYNTAX)

    # DB
    new_user = User(username=username)
    new_user.hash_password(pwd)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"id": new_user.id, "username": new_user.username}), 201, {'Location': url_for('api.get_user', user_id=new_user.id, _external=True)}
