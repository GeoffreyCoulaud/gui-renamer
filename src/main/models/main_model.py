from enum import StrEnum

from gi.repository import GObject  # type: ignore


class MainModel(GObject.Object):
    """MVC model for the main application logic."""

    class Signals(StrEnum):
        NOTIFY_PICKED_FILE_PATHS = "notify::picked-file-paths"
        NOTIFY_RENAMED_FILE_PATHS = "notify::renamed-file-paths"
        NOTIFY_REGEX = "notify::regex"
        NOTIFY_REPLACE_PATTERN = "notify::replace-pattern"
        NOTIFY_APPLY_TO_FULL_PATH = "notify::apply-to-full-path"

    picked_file_paths: list[str] = GObject.Property(type=object)
    renamed_file_paths: list[str] = GObject.Property(type=object)
    regex: str = GObject.Property(type=str, default="")
    replace_pattern: str = GObject.Property(type=str, default="")
    apply_to_full_path: bool = GObject.Property(type=bool, default=False)
