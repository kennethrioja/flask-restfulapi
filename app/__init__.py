from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth


db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()
users = [
    {
        "joueur": 1,
        "email": "first@example.com",
        "firstName": "John",
        "lastName": "Doe",
    }
]
logs = [
    {
        "id": 1,
        "joueur": 26051990,
        "timestamp": "2023-04-18T10:12:51.832Z",
        "sequence": 1,
        "nomSalle": "consentement",
        "action": "connexion",
        "reponseJoueur": "",
        "typeAction": "systeme",
        "erreurJoueur": ""
    }
]

# GLOBAL VARIABLES
ERR_JSON = "Not a json object"
ERR_USERS_NFIELD = "Users - Missing required fields (email, firstName, lastName)"
ERR_USERS_KEYSYNTAX = "Users - Incorrect key syntax (email, firstName, lastName)"
ERR_USERS_EMAILSYNTAX = "Users - Incorrect email syntax"
ERR_USERS_NAMELEN = "Users - firstName and lastName values must be at least 2 characters long"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/tsadk/api')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app
