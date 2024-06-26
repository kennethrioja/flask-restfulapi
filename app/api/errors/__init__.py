from flask import Blueprint

bp = Blueprint("errors", __name__)

ERR_JSON = "Not a json object"
ERR_USERS_NFIELD = "Users - Missing required fields (username, pwd)"
ERR_USERS_DUPLICATE = "Users - This username already exists, please choose another one"
ERR_USERS_KEYSYNTAX = "Users - Incorrect key syntax (username, pwd)"
ERR_USERS_EMAILSYNTAX = "Users - Incorrect email syntax"
ERR_USERS_NAMELEN = "Users - username must be at least 2 characters long"
ERR_LOGS_NFIELD = "Logs - Missing required fields (LIST HERE)"
ERR_LOGS_KEYSYNTAX = "Logs - Incorrect key syntax (LIST HEREJ)"
ERR_LOGS_NOUSERSFOUND = "Logs – User not found from userID"
ERR_LOGS_INVALIDUSERID = "Logs - You are not allowed to post logs for another user"


from app.api.errors import handlers
