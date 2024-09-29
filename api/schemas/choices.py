from enum import Enum


class FieldTypes(Enum):
    SHORT_TEXT = "short_text"
    PARAGRAPH = "paragraph"
    MULTI_CHOICE = "multi_choice"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    FILE = "file"
    DATE = "date"
    DATETIME = "datetime"

    def __str__(self):
        return f"{self.__class__.__name__}.{self.name}"
