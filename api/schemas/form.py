import uuid
from datetime import datetime
from marshmallow import (
    fields as mm_fields,
    pre_load,
    validate,
    validates_schema,
    Schema,
    ValidationError,
    EXCLUDE,
)
from .choices import FieldTypes
from .fields import ObjectIdField


class FieldSchema(Schema):
    id = mm_fields.Str(load_default=lambda: str(uuid.uuid4()))
    label = mm_fields.Str(required=True)
    field_type = mm_fields.Enum(FieldTypes, by_value=mm_fields.Str())
    description = mm_fields.Str(required=False)
    required = mm_fields.Bool(required=True)
    options = mm_fields.List(mm_fields.Str(), required=False)

    @validates_schema
    def validate_options(self, data, **kwargs):
        required_field_types = [
            FieldTypes.MULTI_CHOICE,
            FieldTypes.DROPDOWN,
        ]
        if data["field_type"] in required_field_types and not bool(
            data.get("options", [])
        ):
            raise ValidationError(
                f"Options are required for multi choice fields (dropdown, checkbox etc)."
            )



class SectionSchema(Schema):
    id = mm_fields.Str(load_default=lambda: str(uuid.uuid4()))
    title = mm_fields.Str(required=False)
    description = mm_fields.Str(required=False)
    fields = mm_fields.List(mm_fields.Nested(FieldSchema), required=False)

    class Meta:
        dump_only = ["created_at"]


class UpdateSectionSchema(Schema):
    id = mm_fields.Str(required=True)
    fields = mm_fields.List(mm_fields.Nested(FieldSchema), required=False)


class CreateFormSchema(Schema):
    title = mm_fields.Str(required=True)
    description = mm_fields.Str(required=False)
    sections = mm_fields.List(mm_fields.Nested(SectionSchema), required=True)
    metadata = mm_fields.Dict(required=False)
    quota = mm_fields.Integer(
        required=False,
        load_default=1000,
        validate=validate.Range(
            min=0, error="quota is invalid, it should be a positive integer."
        ),
    )
    is_open = mm_fields.Bool(load_default=True, required=False)
    created_at = mm_fields.DateTime(load_default=lambda: datetime.now())



class UpdateFormSchema(CreateFormSchema):
    sections = mm_fields.List(mm_fields.Nested(UpdateSectionSchema), required=True)


class FormSchema(CreateFormSchema):
    _id = ObjectIdField()
    created_by = mm_fields.Str(load_default="1")

    class Meta:
        unknown = EXCLUDE


class FormTimeSeriesSchema(Schema):
    _id = mm_fields.Date()
    total_responses = mm_fields.Integer()
