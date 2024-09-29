from marshmallow import fields as mm_fields, Schema


class APIErrorSchema(Schema):
    message = mm_fields.Str(required=False)
