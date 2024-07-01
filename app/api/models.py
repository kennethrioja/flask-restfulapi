from typing import Optional
from app import db
from passlib.apps import custom_app_context as pwd_context
from config import Config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    BadSignature, SignatureExpired
import sqlalchemy as sa
import sqlalchemy.orm as so


class User(db.Model):
    __tablename__ = "users"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    pwd_hash: so.Mapped[str] = so.mapped_column(sa.String(128))
    role: so.Mapped[str] = so.mapped_column(sa.String(32),
                                            default=lambda: "user")

    logs: so.WriteOnlyMapped["Log"] = so.relationship(back_populates="user")

    def __repr__(self):
        return "<User {}>".format(self.id)

    def hash_password(self, pwd):
        self.pwd_hash = pwd_context.encrypt(pwd)

    def verify_password(self, pwd):
        return pwd_context.verify(pwd, self.pwd_hash)

    def generate_auth_token(self, expiration=Config.TOKEN_EXPIRATION_SEC):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user


class Log(db.Model):
    __tablename__ = "logs"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    userID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                              index=True)
    timestamp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    sequence: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    roomName: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    actionNature: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    actionType: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    userAnswer: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2048))
    userError: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))

    user: so.Mapped[User] = so.relationship(back_populates="logs")

    def __repr__(self):
        return "<Logs {}>".format(self.user)
