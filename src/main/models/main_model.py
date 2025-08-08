class MainModel:
    """MVC model for the main application logic."""

    def __init__(self):
        self.picked_file_paths: list[str] = []
        self.renamed_file_paths: list[str] = []
        self.regex: str = ""
        self.replace_pattern: str = ""
