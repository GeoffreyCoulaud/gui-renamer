# ruff: noqa: E402

import sys

import gi  # type: ignore

from main.enums.action_names import ActionNames
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

VARIANT_TYPE_STRING = GLib.VariantType.new("s")


class App(Adw.Application):
    """Main application class that initializes the application and its components."""

    __model: MainModel
    __controller: MainWindowController
    __window: MainWindow

    __quit_action: Gio.Action
    __pick_files_action: Gio.Action
    __rename_target_action: Gio.Action

    def __init__(self) -> None:
        super().__init__(
            application_id=constants.APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.__model = MainModel()
        self.__register_actions()

    def __register_actions(self) -> None:
        # Quit action
        self.__quit_action = Gio.SimpleAction.new(name=ActionNames.QUIT)
        self.__quit_action.connect("activate", lambda *_: self.quit())
        self.add_action(self.__quit_action)
        self.set_accels_for_action("app.quit", ["<primary>q"])

        # Rename target action
        self.__rename_target_action = Gio.PropertyAction.new(
            name=ActionNames.RENAME_TARGET,
            object=self.__model,
            property_name="rename-target",
        )
        self.add_action(self.__rename_target_action)

        # Pick files action
        self.__pick_files_action = Gio.SimpleAction.new(name=ActionNames.PICK_FILES)
        self.add_action(self.__pick_files_action)

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
            + InboundProperty(
                source=self.__model,
                source_property="rename-target",
                target_property="rename_target",
            )
        )
        self.__controller = MainWindowController(
            model=self.__model,
            view=self.__window,
        )
        self.__controller.present()


def main():
    """The application's entry point."""
    app = App()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
