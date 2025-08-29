from gi.repository import Adw, Gdk, GObject, Gtk  # type: ignore

from pattern_renamer.main.build_constants import PROFILE
from pattern_renamer.main.types.app_state import AppState
from pattern_renamer.main.types.mistakes import Mistake
from pattern_renamer.main.ui.empty_page import EmptyPage
from pattern_renamer.main.ui.renamed_page import RenamedPage
from pattern_renamer.main.ui.renaming_page import RenamingPage
from pattern_renamer.main.ui.widget_builder.widget_builder import (
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

    renamed_paths: list[str] = GObject.Property(type=object)  # type: ignore
    mistakes: list[Mistake] = GObject.Property(type=object)  # type: ignore
    rename_target: str = GObject.Property(type=str)  # type: ignore

    # --- Bidirectional properties

    # Can be set from the file picker (inbound) or drag and drop (outbound)
    picked_paths: list[str] = GObject.Property(type=object)  # type: ignore

    # ---

    __navigation: Adw.NavigationView

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()
        self.__setup_drop_target()

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
            + InboundProperty(
                source=self,
                source_property="mistakes",
                target_property="mistakes",
                flags=GObject.BindingFlags.SYNC_CREATE,
            )
        )
        self.__navigation = build(
            Adw.NavigationView + Children(empty_page, renamed_page, renaming_page)
        )
        self.set_content(self.__navigation)
        self.set_default_size(800, 600)

        if PROFILE == "development":
            self.add_css_class("devel")

    def __setup_drop_target(self) -> None:
        """Setup drop target to accept file drops"""
        drop_target = Gtk.DropTarget.new(type=Gdk.FileList, actions=Gdk.DragAction.COPY)
        drop_target.connect("drop", self.__on_files_dropped)
        self.add_controller(drop_target)

    def __update_navigation(self) -> None:
        """Update the navgation view based on the current app state"""

        # Empty page (always on the bottom)
        visible_tag = self.__navigation.get_visible_page_tag()  # type: ignore
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

    def __on_files_dropped(
        self,
        _drop_target: Gtk.DropTarget,
        dropped: Gdk.FileList,
        _x: float,
        _y: float,
    ) -> None:
        """Handle dropped text"""
        paths = [
            path
            for file in dropped.get_files()
            if (path := file.get_path()) is not None
        ]
        if not paths:
            return
        self.picked_paths = paths
