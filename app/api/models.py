from typing import Optional
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    firstName: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    lastName: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.firstName)


class Logs(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    joueur: so.Mapped[int] = so.mapped_column(sa.Integer)
    timestamp: so.Mapped[str] = so.mapped_column(sa.String(32))
    sequence: so.Mapped[int] = so.mapped_column(sa.Integer)
    nomSalle: so.Mapped[str] = so.mapped_column(sa.String(32))
    action: so.Mapped[str] = so.mapped_column(sa.String(32))
    reponseJoueur: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    typeAction: so.Mapped[str] = so.mapped_column(sa.String(32))
    erreurJoueur: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))

    def __repr__(self):
        return '<Logs {}>'.format(self.joueur)
