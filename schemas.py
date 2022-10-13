from marshmallow import Schema, fields


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class MovieSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Integer()
    genre_id = fields.Integer()
    genre = fields.Nested(GenreSchema)
    director_id = fields.Integer()
    director = fields.Nested(DirectorSchema)








