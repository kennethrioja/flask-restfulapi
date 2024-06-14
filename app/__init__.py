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
    app.register_blueprint(api_bp, url_prefix='/tsadk/api')

    from app.api.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app
