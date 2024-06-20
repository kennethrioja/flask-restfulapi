import os
import sqlite3

# load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
connection = sqlite3.connect("cache.db", timeout=10)


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
