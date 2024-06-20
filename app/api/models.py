from typing import Optional
from app import db
from passlib.apps import custom_app_context as pwd_context
import sqlalchemy as sa
import sqlalchemy.orm as so


class User(db.Model):
    __tablename__ = "users"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    pwd_hash: so.Mapped[str] = so.mapped_column(sa.String(128))
    # email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
    #                                          unique=True)

    logs: so.WriteOnlyMapped["Log"] = so.relationship(back_populates="user")

    def __repr__(self):
        return "<User {}>".format(self.id)

    def hash_password(self, pwd):
        self.pwd_hash = pwd_context.encrypt(pwd)

    def verify_password(self, pwd):
        return pwd_context.verify(pwd, self.pwd_hash)


class Log(db.Model):
    __tablename__ = "logs"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    userID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                              index=True)
    timestamp: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    # sequence: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    # roomName: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    # actionNature: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    # actionType: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    # userAnswer: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2048))
    # userError: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))

    user: so.Mapped[User] = so.relationship(back_populates="logs")

    def __repr__(self):
        return "<Logs {}>".format(self.joueur)
