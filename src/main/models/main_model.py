import re
from pathlib import Path

from gi.repository import GObject  # type: ignore

from main.enums.app_state import AppState
from main.enums.rename_target_action_options import RenameTarget  # type: ignore


class MainModel(GObject.Object):
    """MVC model for the main application logic."""

    __picked_paths: list[str]

    @GObject.Property(type=object)
    def picked_paths(self) -> list[str]:
        return self.__picked_paths

    @picked_paths.setter
    def picked_paths_setter(self, value: list[str, str]) -> None:
        self.__picked_paths = value
        self.is_apply_enabled = bool(value)
        self.app_state = AppState.RENAMING if value else AppState.EMPTY
        self.recompute_renamed_paths()

    __regex: str = ""

    @GObject.Property(type=str, default="")
    def regex(self) -> str:
        return self.__regex

    @regex.setter
    def regex_setter(self, value: str) -> None:
        self.__regex = value
        self.recompute_renamed_paths()

    __replace_pattern: str = ""

    @GObject.Property(type=str, default="")
    def replace_pattern(self) -> str:
        return self.__replace_pattern

    @replace_pattern.setter
    def replace_pattern_setter(self, value: str) -> None:
        self.__replace_pattern = value
        self.recompute_renamed_paths()

    __rename_target: RenameTarget = RenameTarget.NAME

    @GObject.Property(type=str, default=RenameTarget.NAME)
    def rename_target(self) -> str:
        return self.__rename_target

    @rename_target.setter
    def rename_target_setter(self, value: RenameTarget) -> None:
        self.__rename_target = value
        self.recompute_renamed_paths()

    renamed_paths: list[str] = GObject.Property(type=object)
    is_apply_enabled: bool = GObject.Property(type=bool, default=False)
    is_undo_enabled: bool = GObject.Property(type=bool, default=False)
    app_state: AppState = GObject.Property(type=str, default=AppState.EMPTY)

    # ---

    def __init__(self):
        super().__init__()
        self.__picked_paths = []

    def _rename_using_full_path(self, path: str) -> str:
        """Rename the full path based on the regex and replace pattern."""
        return re.sub(self.regex, self.replace_pattern, path)

    def _rename_using_name(self, path: str) -> str:
        """Rename the file name based on the regex and replace pattern."""
        p = Path(path)
        name = re.sub(self.regex, self.replace_pattern, p.name)
        return str(p.parent / name)

    def _rename_using_stem(self, path: str) -> str:
        """Rename the file stem based on the regex and replace pattern."""
        p = Path(path)
        name = p.with_stem(f"{re.sub(self.regex, self.replace_pattern, p.stem)}")
        return str(p.parent / name)

    def recompute_renamed_paths(self) -> None:
        """Recompute the renamed file paths based on the current regex and replace pattern."""

        transform: callable[[str], str]
        match self.rename_target:
            case RenameTarget.FULL:
                transform = self._rename_using_full_path
            case RenameTarget.NAME:
                transform = self._rename_using_name
            case RenameTarget.STEM:
                transform = self._rename_using_stem
            case _:
                raise ValueError(f"Unknown rename target: {self.rename_target}")

        self.renamed_paths = [transform(p) for p in self.picked_paths]

    def apply_renaming(self) -> None:
        """Apply the renaming to the picked paths"""

        print("PLACEHOLDER - Should rename")
        # TODO implement the actual renaming logic

        self.app_state = AppState.RENAMED
        self.is_undo_enabled = True

    def undo_renaming(self) -> None:
        """Undo the rename operation."""

        print("PLACEHOLDER - Should undo renaming")
        # TODO implement the actual undo logic

        self.app_state = AppState.RENAMING
        self.is_undo_enabled = False
