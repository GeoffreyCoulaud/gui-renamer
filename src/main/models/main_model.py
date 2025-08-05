from pathlib import Path


class MainModel:
    """MVC model for the main application logic."""

    def __init__(self):
        self.picked_file_paths = list[Path]()
        self.renamed_file_paths = list[Path]()
        self.regex_text = ""
