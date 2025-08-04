from pathlib import Path


class MainModel:
    """MVC model for the main application logic."""

    def __init__(self):
        self.file_paths_to_rename = list[Path]()
