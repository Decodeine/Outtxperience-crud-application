
from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)
    isbn = fields.Str(required=True, validate=validate.Length(equal=13))