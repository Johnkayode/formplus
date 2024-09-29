import bson
from datetime import datetime, date
from marshmallow import ValidationError, fields, missing


class ObjectIdField(fields.Field):
    def _deserialize(self, value, attr, data):
        try:
            return bson.ObjectId(value)
        except Exception:
            raise ValidationError("invalid ObjectId `%s`" % value)

    def _serialize(self, value, attr, obj):
        if value is None:
            return missing
        return str(value)


class ValueField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if (
            isinstance(value, str)
            or isinstance(value, list)
            or isinstance(value, int)
            or isinstance(value, datetime)
            or isinstance(value, date)
        ):
            return value
        else:
            raise ValidationError(f"Invalid Value Type {type(value)}")
