from enum import StrEnum

from gi.repository import Adw, GObject  # type: ignore

from main.components.empty_page import EmptyPage
from main.components.renaming_page import RenamingPage
from main.widget_builder.widget_builder import (
    Children,
    InboundProperty,
    OutboundProperty,
    Reemit,
    build,
)


class MainWindow(Adw.ApplicationWindow):
    """
    MVC view for the main window of the application.
    It reemits signals to the controller from the inner components.
    """

    class Signals(StrEnum):
        PICK_FILES = "pick-files"
        NOTIFY_PICKED_PATHS = "notify::picked-paths"
        NOTIFY_RENAMED_PATHS = "notify::renamed-paths"
        NOTIFY_REGEX = "notify::regex"
        NOTIFY_REPLACE_PATTERN = "notify::replace-pattern"
        NOTIFY_APPLY_TO_FULL_PATH = "notify::apply-to-full-path"

    # --- PyGobject things

    @GObject.Signal(name=Signals.PICK_FILES)
    def signal_pick_files(self):
        pass

    picked_paths: list[str] = GObject.Property(type=object)
    renamed_paths: list[str] = GObject.Property(type=object)
    regex = GObject.Property(type=str, default="")
    replace_pattern = GObject.Property(type=str, default="")
    apply_to_full_path: bool = GObject.Property(type=bool, default=False)

    # ---

    def __build(self) -> None:
        empty_page = build(
            EmptyPage
            + Reemit(
                signal=EmptyPage.Signals.PICK_FILES,
                target=self,
                target_signal=self.Signals.PICK_FILES,
            )
        )
        renaming_page = build(
            RenamingPage
            + InboundProperty(
                source=self,
                source_property="renamed-paths",
                target_property="renamed-paths",
            )
            + InboundProperty(
                source=self,
                source_property="picked-paths",
                target_property="picked-paths",
            )
            + OutboundProperty(
                source_property="regex",
                target=self,
                target_property="regex",
            )
            + OutboundProperty(
                source_property="replace-pattern",
                target=self,
                target_property="replace-pattern",
            )
            + OutboundProperty(
                source_property="apply-to-full-path",
                target=self,
                target_property="apply-to-full-path",
            )
        )
        self.__navigation: Adw.NavigationView = build(
            Adw.NavigationView + Children(empty_page, renaming_page)
        )
        self.set_content(self.__navigation)
        self.set_default_size(800, 600)

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()
        self.connect(self.Signals.NOTIFY_PICKED_PATHS, self.__on_picked_paths_changed)

    def __on_picked_paths_changed(self, _source, paths: list[str]):
        """Update the navigation view based on the current paths."""
        visible_tag = self.__navigation.get_visible_page_tag()
        if paths and visible_tag != RenamingPage.TAG:
            self.__navigation.push_by_tag(RenamingPage.TAG)
        elif (not paths) and visible_tag != EmptyPage.TAG:
            self.__navigation.pop_to_tag(EmptyPage.TAG)
