from gi.repository import Adw, GObject  # type: ignore

from main.components.empty_page import EmptyPage
from main.components.renamed_page import RenamedPage
from main.components.renaming_page import RenamingPage
from main.enums.app_state import AppState
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

    __app_state: AppState = AppState.EMPTY

    @GObject.Property(type=str)
    def app_state(self):
        return self.__app_state

    @app_state.setter
    def app_state_setter(self, state: AppState) -> None:
        self.__app_state = state
        self.__update_navigation()

    picked_paths: list[str] = GObject.Property(type=object)
    renamed_paths: list[str] = GObject.Property(type=object)
    rename_target: str = GObject.Property(type=str)

    # ---

    __navigation: Adw.NavigationView

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

    def __build(self) -> None:
        empty_page = build(EmptyPage)
        renamed_page = build(RenamedPage)
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
            Adw.NavigationView + Children(empty_page, renamed_page, renaming_page)
        )
        self.set_content(self.__navigation)
        self.set_default_size(800, 600)

    def __update_navigation(self) -> None:
        """Update the navgation view based on the current app state"""

        # Empty page (always on the bottom)
        visible_tag = self.__navigation.get_visible_page_tag()
        if self.app_state == AppState.EMPTY and visible_tag != EmptyPage.TAG:
            self.__navigation.pop_to_tag(EmptyPage.TAG)

        # Going to the renaming page (from empty, or back from renamed)
        if self.app_state == AppState.RENAMING and visible_tag != RenamingPage.TAG:
            if visible_tag == RenamedPage.TAG:
                self.__navigation.pop_to_tag(RenamingPage.TAG)
            if visible_tag == EmptyPage.TAG:
                self.__navigation.push_by_tag(RenamingPage.TAG)

        # Going to the renamed page (always on top)
        if self.app_state == AppState.RENAMED and visible_tag != RenamedPage.TAG:
            self.__navigation.push_by_tag(RenamedPage.TAG)
