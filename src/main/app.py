# ruff: noqa: E402

from abc import abstractmethod
import sys
from typing import Callable
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib

from main.components.main_window import MainWindow
import main.constants as constants
from main.controllers.main_window_controller import MainWindowController
from main.models.main_model import MainModel


class BaseApplication(Adw.Application):
    """Base class with commodity methods for the application"""

    def _create_action(
        self,
        name: str,
        callback: Callable,
        param_type: None | str | GLib.VariantType = None,
        shortcuts: None | list[str] = None,
    ) -> None:
        """Create an action with a name, handler and optional shortcuts"""
        if isinstance(param_type, str):
            param_type = GLib.VariantType.new(param_type)
        action = Gio.SimpleAction.new(name, param_type)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts is not None:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    @abstractmethod
    def do_activate(self):
        """Method called when the application is activated"""


class App(BaseApplication):
    """Main application class that initializes the application and its components."""

    def __init__(self):
        super().__init__(
            application_id=constants.APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self._create_action("quit", lambda *_: self.quit(), shortcuts=["<primary>q"])

        # Initialize the main model, view, and controller
        self.__main_model = MainModel()
        self.__main_window: MainWindow
        self.__main_window_controller: MainWindowController

    def do_activate(self):
        self.__main_window = MainWindow(application=self)
        self.__main_window_controller = MainWindowController(
            model=self.__main_model, view=self.__main_window
        )
        self.__main_window_controller.present()


def main():
    """The application's entry point."""
    app = App()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
