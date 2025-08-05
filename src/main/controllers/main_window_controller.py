from typing import cast
from main.signals import Signals
from main.components.main_window import MainWindow
from main.models.main_model import MainModel

from gi.repository import Gtk, GLib, Gio


class MainWindowController:
    """MVC controller for the main window of the application."""

    def __init__(self, model: MainModel, view: MainWindow):
        self.__model = model
        self.__view = view
        self.__view.connect(
            Signals.PICK_FILES,
            self.__on_files_picker_requested,
        )
        self.__view.connect(
            Signals.REGEX_CHANGED,
            self.__on_regex_changed,
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

    def __on_regex_changed(self, _source_object, regex_text: str):
        """Handle the regex text change and update the model."""
        self.__model.regex_text = regex_text
        self.recompute_renamed_paths()
        self.__view.update_renamed_paths(paths=self.__model.renamed_file_paths)

    def recompute_renamed_paths(self):
        """Recompute the renamed paths based on the current regex."""

        # TODO implement the logic to recompute the renamed paths here
        self.__model.renamed_file_paths = self.__model.picked_file_paths.copy()

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
        self.__view.update_picked_paths(paths=self.__model.picked_file_paths)
        self.recompute_renamed_paths()
        self.__view.update_renamed_paths(paths=self.__model.renamed_file_paths)

    def present(self):
        """Present the main window"""
        self.__view.present()
