from enum import StrEnum


class AppState(StrEnum):
    EMPTY = "empty"
    RENAMING = "renaming"
    RENAMED = "renamed"
