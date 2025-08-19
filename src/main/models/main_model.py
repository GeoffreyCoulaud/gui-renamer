from collections import defaultdict
import re
from re import Pattern
from pathlib import Path

from gi.repository import GObject  # type: ignore
from pathvalidate import validate_filepath, ValidationError

from main.enums.app_state import AppState
from main.enums.rename_target import RenameTarget
from main.models.mistakes import (
    DuplicateMistake,
    ExistsMistake,
    InvalidDestinationMistake,
    InvalidRegexMistake,
    Mistake,
)  # type: ignore


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
    mistakes: list[Mistake] = GObject.Property(type=object)

    # ---

    def __init__(self):
        super().__init__()
        self.__picked_paths = []

    def _rename_using_full_path(self, regex: Pattern, path: str) -> str:
        """Rename the full path based on the regex and replace pattern."""
        return regex.sub(self.replace_pattern, path)

    def _rename_using_name(self, regex: Pattern, path: str) -> str:
        """Rename the file name based on the regex and replace pattern."""
        p = Path(path)
        name = regex.sub(self.replace_pattern, p.name)
        return str(p.parent / name)

    def _rename_using_stem(self, regex: Pattern, path: str) -> str:
        """Rename the file stem based on the regex and replace pattern."""
        p = Path(path)
        name = p.with_stem(f"{regex.sub(self.replace_pattern, p.stem)}")
        return str(p.parent / name)

    def recompute_renamed_paths(self) -> None:
        """Recompute the renamed file paths based on the current regex and replace pattern."""

        transform: callable[[Pattern, str], str]
        match self.rename_target:
            case RenameTarget.FULL:
                transform = self._rename_using_full_path
            case RenameTarget.NAME:
                transform = self._rename_using_name
            case RenameTarget.STEM:
                transform = self._rename_using_stem
            case _:
                raise ValueError(f"Unknown rename target: {self.rename_target}")

        # Validate the regex
        try:
            pattern = re.compile(pattern=self.regex)
        except Exception:
            self.mistakes = [InvalidRegexMistake()]
            return

        # Rename the paths
        self.renamed_paths = [transform(pattern, path) for path in self.picked_paths]
        self.check_for_renamed_paths_mistakes()

    def check_for_renamed_paths_mistakes(self) -> None:
        mistakes: list[Mistake] = []
        buckets: defaultdict[str, list[int]] = defaultdict(list)

        for i, renamed_path in enumerate(self.renamed_paths):
            buckets[renamed_path].append(i)

            # Validate that the path is valid for the current platform
            try:
                validate_filepath(file_path=renamed_path, platform="auto")
            except ValidationError:
                mistakes.append(InvalidDestinationMistake(i))
                continue

            # Check if the path already exists
            if Path(renamed_path).exists():
                mistakes.append(ExistsMistake(i))

        # Check for duplicate renamed paths
        for renamed_path, indexes in buckets.items():
            if len(indexes) > 1:
                for index in indexes:
                    mistakes.append(DuplicateMistake(index))

        # Set the mistakes, if any
        self.mistakes = mistakes

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
