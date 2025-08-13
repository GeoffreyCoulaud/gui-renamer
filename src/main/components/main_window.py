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

    @GObject.Signal(name=Signals.PICK_FILES)
    def signal_pick_files(self):
        pass

    # --- Inbound properties

    __picked_file_paths: list[str]

    @GObject.Property(type=object)
    def picked_file_paths(self):
        return self.__picked_file_paths

    @picked_file_paths.setter
    def picked_paths_setter(self, paths: list[str]):
        self.__picked_file_paths = paths

        # Update the navigation view based on the current paths.
        visible_tag = self.__navigation.get_visible_page_tag()
        if paths and visible_tag != RenamingPage.TAG:
            self.__navigation.push_by_tag(RenamingPage.TAG)
        elif (not paths) and visible_tag != EmptyPage.TAG:
            self.__navigation.pop_to_tag(EmptyPage.TAG)

    renamed_file_paths: list[str] = GObject.Property(type=object)
    rename_target: str = GObject.Property(type=str)

    # --- Outbound properties

    regex: str = GObject.Property(type=str, default="")
    replace_pattern: str = GObject.Property(type=str, default="")

    # ---

    __navigation: Adw.NavigationView

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

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
            + InboundProperty(
                source=self,
                source_property="picked-file-paths",
                target_property="picked-file-paths",
            )
            + InboundProperty(
                source=self,
                source_property="renamed-file-paths",
                target_property="renamed-file-paths",
            )
            + InboundProperty(
                source=self,
                source_property="rename-target",
                target_property="rename_target",
            )
        )
        self.__navigation = build(
            Adw.NavigationView + Children(empty_page, renaming_page)
        )
        self.set_content(self.__navigation)
        self.set_default_size(800, 600)
