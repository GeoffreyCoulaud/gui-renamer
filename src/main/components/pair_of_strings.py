from gi.repository import GObject  # type: ignore


class PairOfStrings(GObject.GObject):
    """Simple class to hold a pair of strings"""

    is_first: bool = GObject.Property(type=bool, default=False)
    is_last: bool = GObject.Property(type=bool, default=False)

    first: str = GObject.Property(type=str)
    second: str = GObject.Property(type=str)

    @classmethod
    def new_from_tuple(cls, pair: tuple[str, str]) -> "PairOfStrings":
        """Create a new instance from a tuple of strings."""
        instance = cls()
        instance.first = pair[0]
        instance.second = pair[1]
        return instance
