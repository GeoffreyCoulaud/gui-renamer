from enum import StrEnum
from pathlib import Path
from gi.repository import Adw, Gtk, GObject

from main.components.widget_builder.widget_builder import (
    Children,
    TypedChild,
    build,
    Properties,
    Handlers,
)


class MainWindowSignals(StrEnum):
    """Signals emitted by the MainWindow."""

    FILES_PICKER_REQUESTED = "files-picker-requested"


class MainWindow(Adw.ApplicationWindow):
    """MVC view for the main window of the application."""

    @GObject.Signal(name=MainWindowSignals.FILES_PICKER_REQUESTED)
    def files_picker_requested(self):
        """Signal emitted when the file picker button is clicked."""

    def __build(self):
        """Build the main window layout"""

        header_bar_title = build(Adw.WindowTitle + Properties(title="Renamer"))
        header_bar = build(Adw.HeaderBar + Properties(title_widget=header_bar_title))

        file_picker_button = build(
            Gtk.Button
            + Properties(css_classes=[".suggested-action"])
            + Handlers(clicked=self.__on_files_picker_clicked)
            + Children(
                Adw.ButtonContent
                + Properties(
                    icon_name="document-open-symbolic",
                    label="Select files to rename",
                )
            )
        )
        self.__file_paths_view = build(Gtk.ListBox)
        content_area = build(
            Gtk.Box
            + Properties(orientation=Gtk.Orientation.VERTICAL)
            + Children(
                file_picker_button,
                self.__file_paths_view,
            )
        )

        self.set_content(
            build(
                Adw.ToolbarView
                + TypedChild("top", header_bar)
                + TypedChild("content", content_area)
            )
        )
        self.set_default_size(800, 600)

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

    def __on_files_picker_clicked(self, _emitter) -> None:
        """Emit signal when files picker button is clicked"""
        self.emit(MainWindowSignals.FILES_PICKER_REQUESTED)

    def update_files_view(self, file_paths: list[Path]) -> None:
        """Update the files view with the file paths to rename."""
        self.__file_paths_view.remove_all()
        for file_path in file_paths:
            # TODO better display of file paths, right now just a label
            label = build(Gtk.Label + Properties(label=str(file_path)))
            self.__file_paths_view.append(label)
