from marshmallow import ValidationError
from schemas.choices import FieldTypes


class FieldValidator:
    """
    Validate field types.
    """

    def validate_field(self, field, value):
        str_required_field_types = [
            FieldTypes.SHORT_TEXT.value,
            FieldTypes.PARAGRAPH.value,
            FieldTypes.FILE.value,
        ]

        if field["field_type"] in str_required_field_types and not isinstance(
            value, str
        ):
            raise ValidationError(f"Field {field['label']} should be a string.")

        if field["field_type"] == FieldTypes.DROPDOWN.value:
            options = field.get("options", [])
            if not isinstance(value, int) or not (0 <= value < len(options)):
                raise ValidationError(f"Invalid index for field '{field['label']}'.")

        if field["field_type"] == FieldTypes.CHECKBOX.value and not isinstance(value, bool):
            raise ValidationError(f"Invalid value for field {field['label']}.")

        if field["field_type"] == FieldTypes.MULTI_CHOICE.value and not isinstance(
            value, list
        ):
            options = field.get("options", [])
            if not isinstance(value, list):
                raise ValidationError(f"Field '{field['label']}' must be a list.")
            for index in value:
                if not isinstance(index, int) or not (0 <= index < len(options)):
                    raise ValidationError(
                        f"Invalid index {index} in multiselect field '{field['label']}'."
                    )


class FormValidator:
    """
    Validate form and fields.
    """

    def __init__(self, form):
        self.form = form
        self.errors = {}

    def validate_submission(self, submission):
        for section in self.form["sections"]:
            section_id = section["id"]

            section_fields = section.get("fields", [])

            # Ignore sections with fields
            if not section_fields:
                continue

            sections = submission.get("sections", {})
            section_data = sections.get(section_id, {})
            for field in section_fields:
                field_id = field["id"]
                field_value = section_data.get(field_id, None)

                # Validate required fields
                if field["required"] and (field_value is None or field_value == ""):
                    self.errors[field_id] = f"Field {field['label']} is required."
                    continue

                try:
                    FieldValidator().validate_field(field, field_value)
                except ValidationError as e:
                    self.errors[field_id] = str(e)

        if self.errors:
            raise ValidationError(self.errors)
