from gi.repository import Adw, GObject

from main.components.empty_page import EmptyPage
from main.components.renaming_page import RenamingPage
from main.widget_builder.widget_builder import (
    Children,
    InboundProperty,
    Properties,
    OutboundProperty,
    Reemit,
    TypedChild,
    build,
)
from main.signals import Signals


class MainWindow(Adw.ApplicationWindow):
    """
    MVC view for the main window of the application.
    It reemits signals to the controller from the inner components.
    """

    # --- PyGobject things

    @GObject.Signal(name=Signals.PICK_FILES)
    def signal_pick_files(self):
        pass

    __picked_paths: list[str]

    @GObject.Property(type=object)
    def picked_paths(self) -> list[str]:
        return self.__picked_paths

    @picked_paths.setter
    def picked_paths(self, paths: list[str]):
        self.__picked_paths = paths
        self.__on_picked_paths_changed()

    __renamed_paths: list[str]

    @GObject.Property(type=object)
    def renamed_paths(self) -> list[str]:
        return self.__renamed_paths

    @renamed_paths.setter
    def renamed_paths(self, paths: list[str]):
        self.__renamed_paths = paths

    __regex: list[str]

    @GObject.Property(type=object)
    def regex(self) -> list[str]:
        return self.__regex

    @regex.setter
    def regex(self, paths: list[str]):
        self.__regex = paths

    __replace_pattern: list[str]

    @GObject.Property(type=object)
    def replace_pattern(self) -> list[str]:
        return self.__replace_pattern

    @replace_pattern.setter
    def replace_pattern(self, paths: list[str]):
        self.__replace_pattern = paths

    # ---

    def __build(self):
        header = Adw.HeaderBar + Children(Adw.WindowTitle + Properties(title="Renamer"))
        empty_page = build(EmptyPage + Reemit(Signals.PICK_FILES, self))
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
        )
        self.__navigation: Adw.NavigationView = build(
            Adw.NavigationView + Children(empty_page, renaming_page)
        )
        content = build(
            Adw.ToolbarView
            + TypedChild("top", header)
            + TypedChild("content", Adw.ClampScrollable + Children(self.__navigation))
        )
        self.set_content(content)
        self.set_default_size(800, 600)

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

    def __on_picked_paths_changed(self, *_args):
        """Update the navigation view based on the current paths."""
        if self.picked_paths:
            self.__navigation.push_by_tag(RenamingPage.TAG)
        else:
            self.__navigation.pop_to_tag(EmptyPage.TAG)
