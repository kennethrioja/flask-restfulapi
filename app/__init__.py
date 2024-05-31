from flask import Flask, Blueprint
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()
bp = Blueprint('api', __name__)
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


from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)


from app import routes
