from enum import StrEnum


class Signals(StrEnum):
    """Signals used in the application."""

    FILES_PICKER_REQUESTED = "files-picker-requested"
    REGEX_CHANGED = "regex-changed"
