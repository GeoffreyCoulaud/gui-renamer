from abc import ABC


class Mistake(ABC):
    """
    Class representing a user mistake.

    Mistakes are correctable errors that the user can fix to proceed with the renaming.<br/>
    Renaming cannot be applied if there are mistakes.
    """

    message: str

    def __init__(self, message: str):
        self.message = message


class InvalidRegexMistake(Mistake):
    """Mistake raised when the user provides an invalid regex"""

    def __init__(self):
        super().__init__(message="Provided regex is invalid")


class RenameDestinationMistake(Mistake, ABC):
    """Base class for mistakes related to rename destination paths"""

    culprit_index: int

    def __init__(self, message: int, culprit_index: int):
        super().__init__(message=message)
        self.culprit_index = culprit_index


class InvalidDestinationMistake(RenameDestinationMistake):
    """Mistake raised when the rename destination is invalid for the current platform"""

    def __init__(self, culprit_index: int):
        super().__init__(
            message="Rename destination is invalid",
            culprit_index=culprit_index,
        )


class DuplicateMistake(RenameDestinationMistake):
    """Mistake raised when several items would be renamed to the same destination path"""

    def __init__(self, culprit_index: int):
        super().__init__(
            message="Several items would be renamed to the same destination path",
            culprit_index=culprit_index,
        )


class ExistsMistake(RenameDestinationMistake):
    """Mistake raised when the rename destination already exists"""

    def __init__(self, culprit_index: int):
        super().__init__(
            message="Renaming conflicts with an existing path",
            culprit_index=culprit_index,
        )
