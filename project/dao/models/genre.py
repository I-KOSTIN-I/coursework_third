from marshmallow import Schema, fields
from project.dao.models.base import BaseMixin
from project.setup_db import db


class Genre(BaseMixin, db.Model):
    __tablename__ = "genres"

    name = db.Column(db.String(255), unique=True, nullable=False)


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
