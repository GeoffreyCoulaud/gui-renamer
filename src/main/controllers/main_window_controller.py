from pathlib import Path
from typing import cast
from main.components.main_window import MainWindow, MainWindowSignals
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
        self.__files_picker = Gtk.FileDialog(
            title="Select files to rename",
            modal=True,
        )

    def __on_files_picker_requested(self, _source_object):
        """Make the user select files to rename."""
        self.__files_picker.open_multiple(
            parent=self.__view.get_root(),
            callback=self.__on_files_picked,
        )

    def __on_files_picked(self, _source_object, result: Gio.AsyncResult):
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
        self.__view.update_files_view(file_paths=self.__model.file_paths_to_rename)

    def present(self):
        """Present the main window"""
        self.__view.present()
