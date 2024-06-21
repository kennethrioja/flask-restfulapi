from flask import Blueprint

bp = Blueprint("auth", __name__)

# ACL
access_rules = {
    "user1": ["/api/resource1"],
    "user2": ["/api/resource2", "/api/resource3", "/api/resource4", "/api/resource5", "/api/resource6", "/api/resource7", "/api/resource8", "/api/resource9", "/api/resource10"]
}

from app.api.auth import auth, decorators
