from enum import StrEnum


class ActionNames(StrEnum):
    QUIT = "quit"
    PICK_FILES = "pick-files"
    APPLY_RENAMING = "apply-renaming"
    UNDO_RENAMING = "undo-renaming"

    # Stateful actions
    RENAME_TARGET = "rename-target"
    REGEX = "regex"
    REPLACE_PATTERN = "replace-pattern"
