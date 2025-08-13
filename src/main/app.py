# ruff: noqa: E402

import sys
from typing import Callable

import gi  # type: ignore

from main.widget_builder.widget_builder import (  # type: ignore
    Arguments,
    InboundProperty,
    OutboundProperty,
    build,
)

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib  # type: ignore

import main.constants as constants
from main.components.main_window import MainWindow
from main.controllers.main_window_controller import MainWindowController
from main.models.main_model import MainModel


class App(Adw.Application):
    """Main application class that initializes the application and its components."""

    __model: MainModel
    __controller: MainWindowController
    __window: MainWindow

    def __init__(self) -> None:
        super().__init__(
            application_id=constants.APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self._create_action(
            name="quit",
            callback=lambda *_: self.quit(),
            shortcuts=["<primary>q"],
        )
        self.__model = MainModel()

    def do_activate(self):
        self.__window = build(
            MainWindow
            + Arguments(application=self)
            + OutboundProperty(
                source_property="regex",
                target=self.__model,
                target_property="regex",
            )
            + OutboundProperty(
                source_property="replace-pattern",
                target=self.__model,
                target_property="replace-pattern",
            )
            + OutboundProperty(
                source_property="apply-to-full-path",
                target=self.__model,
                target_property="apply-to-full-path",
            )
            + InboundProperty(
                source=self.__model,
                source_property="picked-file-paths",
                target_property="picked-file-paths",
            )
            + InboundProperty(
                source=self.__model,
                source_property="renamed-file-paths",
                target_property="renamed-file-paths",
            )
        )
        self.__controller = MainWindowController(
            model=self.__model,
            view=self.__window,
        )
        self.__controller.present()

    def _create_action(
        self,
        name: str,
        callback: Callable,
        param_type: None | GLib.VariantType = None,
        shortcuts: None | list[str] = None,
    ) -> None:
        """Create an action with a name, handler and optional shortcuts"""
        action = Gio.SimpleAction.new(name, param_type)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main():
    """The application's entry point."""
    app = App()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
