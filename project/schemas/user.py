from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    favorite_genre = fields.Str()
