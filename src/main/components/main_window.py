from gi.repository import Adw, GObject  # type: ignore

from main.components.empty_page import EmptyPage
from main.components.renaming_page import RenamingPage
from main.widget_builder.widget_builder import (
    Children,
    InboundProperty,
    build,
)


class MainWindow(Adw.ApplicationWindow):
    """
    MVC view for the main window of the application.
    """

    # --- Inbound properties

    __picked_paths: list[str]

    @GObject.Property(type=object)
    def picked_paths(self):
        return self.__picked_paths

    @picked_paths.setter
    def picked_paths_setter(self, paths: list[str]) -> None:
        self.__picked_paths = paths
        self.__update_navigation()

    renamed_paths: list[str] = GObject.Property(type=object)
    rename_target: str = GObject.Property(type=str)

    # ---

    __navigation: Adw.NavigationView

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

    def __build(self) -> None:
        empty_page = build(EmptyPage)
        renaming_page = build(
            RenamingPage
            + InboundProperty(
                source=self,
                source_property="picked-paths",
                target_property="picked-paths",
                flags=GObject.BindingFlags.SYNC_CREATE,
            )
            + InboundProperty(
                source=self,
                source_property="renamed-paths",
                target_property="renamed-paths",
                flags=GObject.BindingFlags.SYNC_CREATE,
            )
            + InboundProperty(
                source=self,
                source_property="rename-target",
                target_property="rename_target",
                flags=GObject.BindingFlags.SYNC_CREATE,
            )
        )
        self.__navigation = build(
            Adw.NavigationView + Children(empty_page, renaming_page)
        )
        self.set_content(self.__navigation)
        self.set_default_size(800, 600)

    def __update_navigation(self) -> None:
        # Update the navigation view based on the current paths.
        visible_tag = self.__navigation.get_visible_page_tag()
        if self.__picked_paths and visible_tag != RenamingPage.TAG:
            self.__navigation.push_by_tag(RenamingPage.TAG)
        elif (not self.__picked_paths) and visible_tag != EmptyPage.TAG:
            self.__navigation.pop_to_tag(EmptyPage.TAG)
