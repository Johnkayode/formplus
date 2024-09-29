from marshmallow import (
    fields as mm_fields,
    Schema,
    EXCLUDE
)
from .fields import ObjectIdField, ValueField


class CreateFormSubmissionSchema(Schema):
    sections = mm_fields.Dict(
        keys=mm_fields.Str(),
        values=mm_fields.Dict(keys=mm_fields.Str(), values=ValueField()),
        required=True,
    )
    created_at = mm_fields.DateTime()


class FormSubmissionSchema(CreateFormSubmissionSchema):
    _id = ObjectIdField()
    form_id = mm_fields.Str()

    class Meta:
        unknown = EXCLUDE


class FormSubmissionsSchema(Schema):
    count = mm_fields.Integer(dump_default=0)
    submissions = mm_fields.List(mm_fields.Nested(FormSubmissionSchema))
