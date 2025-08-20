import re
from collections import defaultdict
from pathlib import Path
from re import Pattern

from gi.repository import GObject  # type: ignore
from pathvalidate import ValidationError, validate_filepath

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

    # --- Inbound properties

    __picked_paths: list[str]

    @GObject.Property(type=object)
    def picked_paths(self) -> list[str]:
        return self.__picked_paths

    @picked_paths.setter
    def picked_paths_setter(self, value: list[str]) -> None:
        self.__picked_paths = value
        self.recompute()

    __regex: str = ""

    @GObject.Property(type=str, default="")
    def regex(self) -> str:
        return self.__regex

    @regex.setter
    def regex_setter(self, value: str) -> None:
        self.__regex = value
        self.recompute()

    __replace_pattern: str = ""

    @GObject.Property(type=str, default="")
    def replace_pattern(self) -> str:
        return self.__replace_pattern

    @replace_pattern.setter
    def replace_pattern_setter(self, value: str) -> None:
        self.__replace_pattern = value
        self.recompute()

    __rename_target: RenameTarget = RenameTarget.NAME

    @GObject.Property(type=str, default=RenameTarget.NAME)
    def rename_target(self) -> str:
        return self.__rename_target

    @rename_target.setter
    def rename_target_setter(self, value: RenameTarget) -> None:
        self.__rename_target = value
        self.recompute()

    # --- Outbound properties

    renamed_paths: list[str] = GObject.Property(type=object)  # type: ignore
    mistakes: list[Mistake] = GObject.Property(type=object)  # type: ignore
    is_apply_enabled: bool = GObject.Property(type=bool, default=False)  # type: ignore
    is_undo_enabled: bool = GObject.Property(type=bool, default=False)  # type: ignore
    app_state: AppState = GObject.Property(type=str, default=AppState.EMPTY)  # type: ignore

    # ---

    def __init__(self):
        super().__init__()
        self.__picked_paths = []

    def recompute(self) -> None:
        """Recompute the outbound properties based on the inbound properties"""

        # Set the app state
        self.app_state = AppState.RENAMING if self.picked_paths else AppState.EMPTY

        try:
            # Validate the regex
            pattern = re.compile(pattern=self.regex)
        except Exception:
            self.mistakes = [InvalidRegexMistake()]
            self.is_apply_enabled = False
        else:
            # Rename the paths
            self.renamed_paths = (
                list(self.picked_paths)
                if (not self.regex or not self.replace_pattern)
                else [
                    self._rename(
                        regex=pattern,
                        path=path,
                        replace_pattern=self.replace_pattern,
                        target=self.rename_target,
                    )
                    for path in self.picked_paths
                ]
            )
            self.mistakes = self._detect_renamed_paths_mistakes(
                renamed_paths=self.renamed_paths,
                picked_paths=self.picked_paths,
            )
            self.is_apply_enabled = (
                self.regex
                and self.replace_pattern
                and self.picked_paths
                and self.picked_paths != self.renamed_paths
                and not self.mistakes
            )

    def _rename(
        self, regex: Pattern, path: str, replace_pattern: str, target: RenameTarget
    ) -> str:
        """Rename the path based on the regex and replace pattern."""
        match target:
            case RenameTarget.FULL:
                return self._rename_using_full_path(
                    regex=regex, replace_pattern=replace_pattern, path=path
                )
            case RenameTarget.NAME:
                return self._rename_using_name(
                    regex=regex, replace_pattern=replace_pattern, path=path
                )
            case RenameTarget.STEM:
                return self._rename_using_stem(
                    regex=regex, replace_pattern=replace_pattern, path=path
                )
            case _:
                raise ValueError(f"Unknown rename target: {self.rename_target}")

    def _rename_using_full_path(
        self, regex: Pattern, replace_pattern: str, path: str
    ) -> str:
        """Rename the full path based on the regex and replace pattern."""
        return regex.sub(replace_pattern, path)

    def _rename_using_name(
        self, regex: Pattern, replace_pattern: str, path: str
    ) -> str:
        """Rename the file name based on the regex and replace pattern."""
        p = Path(path)
        name = regex.sub(replace_pattern, p.name)
        return str(p.parent / name)

    def _rename_using_stem(
        self, regex: Pattern, replace_pattern: str, path: str
    ) -> str:
        """Rename the file stem based on the regex and replace pattern."""
        p = Path(path)
        name = p.with_stem(f"{regex.sub(replace_pattern, p.stem)}")
        return str(p.parent / name)

    def _detect_renamed_paths_mistakes(
        self, renamed_paths: list[str], picked_paths: list[str]
    ) -> list[Mistake]:
        """Check for mistakes in the renamed paths."""

        mistakes: list[Mistake] = []
        buckets: defaultdict[str, list[int]] = defaultdict(list)

        for i, (picked_path, renamed_path) in enumerate(
            zip(picked_paths, renamed_paths)
        ):
            # Check for duplicates
            if renamed_path in buckets:
                mistakes.append(DuplicateMistake(i))
            buckets[renamed_path].append(i)

            # Validate that the path is valid for the current platform
            try:
                validate_filepath(file_path=renamed_path, platform="auto")
            except ValidationError:
                mistakes.append(InvalidDestinationMistake(i))

            # Check if the path already exists and is not the same as the original
            if renamed_path != picked_path and Path(renamed_path).exists():
                mistakes.append(ExistsMistake(i))

        # Set the mistakes, if any
        return mistakes

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
