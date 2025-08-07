from enum import StrEnum


class Signals(StrEnum):
    """Signals used in the application."""

    PICK_FILES = "files-picker-requested"
    REGEX_CHANGED = "regex-changed"
    REPLACE_PATTERN_CHANGED = "replace-pattern-changed"
