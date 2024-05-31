from flask import Flask
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()
users = [
    {
        "id": 1,
        "email": "first@example.com",
        "firstName": "John",
        "lastName": "Doe",
    }
]
logs = [
    {
        "id": 1,
        "timestamp": "17-05-2024 10:17:00",
        "nomSalle": "Mandur",
        "action": "Run",
    }
]

# GLOBAL VARIABLES
ERR_JSON = "Not a json object"
ERR_USERS_NFIELD = "Users - Missing required fields (email, firstName, lastName)"
ERR_USERS_KEYSYNTAX = "Users - Incorrect key syntax (email, firstName, lastName)"
ERR_USERS_EMAILSYNTAX = "Users - Incorrect email syntax"
ERR_USERS_NAMELEN = "Users - firstName and lastName values must be at least 2 characters long"


from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/tsadk/api')


from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)


if __name__ == '__main__':
    app.run(debug=True)
