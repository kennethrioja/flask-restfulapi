from dotenv import load_dotenv
import os

# load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
