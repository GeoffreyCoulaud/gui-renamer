from pathlib import Path
from typing import cast
from main.components.main_window import MainWindow, MainWindowSignals
from main.components.widget_builder.widget_builder import Properties, build
from main.models.main_model import MainModel

from gi.repository import Gtk, GLib, Gio


class MainWindowController:
    """MVC controller for the main window of the application."""

    def __init__(self, model: MainModel, view: MainWindow):
        self.__model = model
        self.__view = view
        self.__view.connect(
            MainWindowSignals.FILES_PICKER_REQUESTED,
            self.__on_files_picker_requested,
        )
        self.__files_picker: Gtk.FileDialog = build(
            Gtk.FileDialog
            + Properties(
                title="Select files to rename",
                modal=True,
            )
        )

    def __on_files_picker_requested(self):
        """Make the user select files to rename."""
        self.__files_picker.open_multiple(
            parent=self.__view.get_root(),
            callback=self.__on_files_picked,
        )

    def __on_files_picked(self, _source_object, result: Gio.AsyncResult, _data):
        """
        Handle the files picked by the user.

        This is a `Gio.AsyncReadyCallback`<br/>
        https://lazka.github.io/pgi-docs/Gio-2.0/callbacks.html#Gio.AsyncReadyCallback
        """

        try:
            paths_list_model = self.__files_picker.open_multiple_finish(result=result)
        except GLib.Error:
            return

        self.__model.file_paths_to_rename = [
            Path(file_path)
            for i in range(paths_list_model.get_n_items())
            if (
                (file_path := cast(Gio.File, paths_list_model.get_item(i)).get_path())
                is not None
            )
        ]

    def present(self):
        """Present the main window"""
        self.__view.present()
