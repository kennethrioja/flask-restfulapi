import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.api.models import User, Log


@app.api.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so, "db": db, "User": User, "Log": Log}


if __name__ == "__main__":
    app.run(debug=True)
