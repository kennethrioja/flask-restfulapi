from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth


db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix=f"/{Config.APP_NAME}/api")

    from app.api.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app
