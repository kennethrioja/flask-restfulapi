import os
import sqlite3

# load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
connection = sqlite3.connect("cache.db", timeout=10)


class Config:
    APP_NAME = os.environ.get("APP_NAME")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")

    TOKEN_EXPIRATION_SEC = int(os.environ.get("TOKEN_EXPIRATION_SEC"))

    SECRET_KEY = os.environ.get("SECRET_KEY")
