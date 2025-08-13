from enum import StrEnum

from gi.repository import GObject  # type: ignore


class MainModel(GObject.Object):
    """MVC model for the main application logic."""

    __picked_file_paths: list[str]

    @GObject.Property(type=object)
    def picked_file_paths(self) -> list[str]:
        return self.__picked_file_paths

    @picked_file_paths.setter
    def picked_file_paths_setter(self, value: list[str]) -> None:
        self.__picked_file_paths = value
        self.recompute_renamed_paths()

    __renamed_file_paths: list[str]

    @GObject.Property(type=object)
    def renamed_file_paths(self) -> list[str]:
        return self.__renamed_file_paths

    @renamed_file_paths.setter
    def renamed_file_paths_setter(self, value: list[str]) -> None:
        self.__renamed_file_paths = value

    __regex: str

    @GObject.Property(type=str)
    def regex(self) -> str:
        return self.__regex

    @regex.setter
    def regex_setter(self, value: str) -> None:
        self.__regex = value
        self.recompute_renamed_paths()

    __replace_pattern: str

    @GObject.Property(type=str)
    def replace_pattern(self) -> str:
        return self.__replace_pattern

    @replace_pattern.setter
    def replace_pattern_setter(self, value: str) -> None:
        self.__replace_pattern = value
        self.recompute_renamed_paths()

    __apply_to_full_path: bool

    @GObject.Property(type=bool, default=False)
    def apply_to_full_path(self) -> bool:
        return self.__apply_to_full_path

    @apply_to_full_path.setter
    def apply_to_full_path_setter(self, value: bool) -> None:
        self.__apply_to_full_path = value
        self.recompute_renamed_paths()

    # ---

    def recompute_renamed_paths(self) -> None:
        # TODO: Implement the logic to recompute renamed file paths
        self.renamed_file_paths = self.picked_file_paths.copy()
        self.notify("picked-file-paths")
