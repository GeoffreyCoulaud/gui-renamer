from typing import cast

from gi.repository import Gio, GLib, Gtk  # type: ignore

from main.components.main_window import MainWindow
from main.models.main_model import MainModel


class MainWindowController:
    """MVC controller for the main window of the application."""

    __model: MainModel
    __view: MainWindow
    __files_picker: Gtk.FileDialog

    def __init__(self, model: MainModel, view: MainWindow):
        self.__model = model
        self.__view = view
        self.__files_picker = Gtk.FileDialog(title="Select files to rename", modal=True)
        self.__view.connect(
            MainWindow.Signals.PICK_FILES,
            self.__on_files_picker_requested,
        )

    def __on_files_picker_requested(self, _source):
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

        self.__model.picked_file_paths = [
            file_path
            for i in range(paths_list_model.get_n_items())
            if (
                (file_path := cast(Gio.File, paths_list_model.get_item(i)).get_path())
                is not None
            )
        ]
        self.__view.picked_paths = self.__model.picked_file_paths

    def present(self):
        """Present the main window"""
        self.__view.present()
