from gi.repository import Adw, Gtk

from main.components.empty_page import EmptyPage
from main.components.renaming_page import RenamingPage
from main.components.widget_builder.widget_builder import (
    Children,
    TypedChild,
    build,
    Properties,
)


class MainWindow(Adw.ApplicationWindow):
    """MVC view for the main window of the application."""

    def __build(self):
        """Build the main window layout"""

        header_bar_title = build(Adw.WindowTitle + Properties(title="Renamer"))
        header_bar = build(Adw.HeaderBar + Properties(title_widget=header_bar_title))

        self.empty_view = build(EmptyPage + Properties(can_pop=False))
        self.renaming_view = build(RenamingPage)
        self.views = build(
            Adw.NavigationView
            + Children(
                self.empty_view,
                self.renaming_view,
            )
        )
        self.set_content(
            build(
                Adw.ToolbarView
                + TypedChild("top", header_bar)
                + TypedChild("content", self.views)
            )
        )
        self.set_default_size(800, 600)

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

    def __build_path_widget(self, path: str) -> Gtk.ListBoxRow:
        # TODO better display of file paths, right now just a label
        return build(
            Gtk.ListBoxRow
            + Children(
                Gtk.Label
                + Properties(
                    label=path,
                    justify=Gtk.Justification.LEFT,
                )
            )
        )

    def update_picked_paths(self, paths: list[str]):
        """Update the picked paths list with the provided paths."""
        self.__current_paths.remove_all()
        for path in paths:
            item = self.__build_path_widget(path)
            self.__current_paths.append(item)

    def update_renamed_paths(self, paths: list[str]):
        """Update the renamed paths list with the provided paths."""
        self.__new_paths.remove_all()
        for path in paths:
            item = self.__build_path_widget(path)
            self.__new_paths.append(item)
