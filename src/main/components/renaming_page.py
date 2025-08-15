from pathlib import Path
from gi.repository import Adw, Gio, GLib, GObject, Gtk  # type: ignore

from main.components.pair_of_strings import PairOfStrings
from main.components.path_list_item_builder import PathLifeCycleManager
from main.enums.action_names import ActionNames
from main.enums.rename_target_action_options import RenameTarget
from main.widget_builder.widget_builder import (
    Children,
    Handlers,
    Properties,
    TypedChild,
    build,
)


class RenamingPage(Adw.NavigationPage):
    """Component for the renaming page of the application."""

    TAG = "renaming-page"

    # --- Inbound properties

    __picked_paths: list[str]

    @GObject.Property(type=object)
    def picked_paths(self):
        return self.__picked_paths

    @picked_paths.setter
    def picked_paths_setter(self, paths: list[str]) -> None:
        self.__picked_paths = paths
        self.__update_path_pairs_model()

    __renamed_paths: list[str]

    @GObject.Property(type=object)
    def renamed_paths(self):
        return self.__renamed_paths

    @renamed_paths.setter
    def renamed_paths_setter(self, paths: list[str]) -> None:
        self.__renamed_paths = paths
        self.__update_path_pairs_model()

    __rename_target: RenameTarget

    @GObject.Property(type=str)
    def rename_target(self):
        return self.__rename_target

    @rename_target.setter
    def rename_target_setter(self, rename_target: RenameTarget) -> None:
        self.__rename_target = rename_target
        self.__update_path_pairs_model()

    # ---

    __path_pairs_model: Gio.ListStore
    __picked_paths_signal_factory: Gtk.SignalListItemFactory
    __picked_paths_lifecycle_manager: PathLifeCycleManager
    __renamed_paths_signal_factory: Gtk.SignalListItemFactory
    __renamed_paths_lifecycle_manager: PathLifeCycleManager

    def __get_menu_model(self) -> Gio.Menu:
        # Create a radio menu with 3 items for rename target selection.
        rename_target_action = f"app.{ActionNames.RENAME_TARGET}"
        full = Gio.MenuItem.new(label="Full path")
        full.set_action_and_target_value(
            action=rename_target_action,
            target_value=GLib.Variant.new_string(RenameTarget.FULL),
        )
        name = Gio.MenuItem.new(label="File name")
        name.set_action_and_target_value(
            action=rename_target_action,
            target_value=GLib.Variant.new_string(RenameTarget.NAME),
        )
        stem = Gio.MenuItem.new(label="File name, without extention")
        stem.set_action_and_target_value(
            action=rename_target_action,
            target_value=GLib.Variant.new_string(RenameTarget.STEM),
        )

        # Create a Gio.Menu and append the items.
        menu = Gio.Menu()
        menu.append_item(stem)
        menu.append_item(name)
        menu.append_item(full)

        return menu

    def __build(self) -> None:
        margin = 12
        BOXED_LIST_PROPERTIES = Properties(
            css_classes=["boxed-list"],
            selection_mode=Gtk.SelectionMode.NONE,
        )

        # Header and menu
        menu_button = Gtk.MenuButton + Properties(
            icon_name="open-menu-symbolic", menu_model=self.__get_menu_model()
        )
        header = (
            Adw.HeaderBar
            + Children(Adw.WindowTitle + Properties(title="Renamer"))
            + TypedChild("end", menu_button)
        )

        # Regex section
        regex_editable = build(
            Adw.EntryRow
            + Properties(title="Regex Pattern", css_classes=["monospace"])
            + Handlers(changed=self.__on_regex_changed)
        )
        replace_pattern_editable = build(
            Adw.EntryRow
            + Properties(title="Replace Pattern", css_classes=["monospace"])
            + Handlers(changed=self.__on_replace_pattern_changed)
        )
        regex_section = build(
            Gtk.ListBox
            + BOXED_LIST_PROPERTIES
            + Properties(
                margin_top=margin,
                margin_bottom=margin / 2,
                margin_start=margin,
                margin_end=margin,
            )
            + Children(
                regex_editable,
                replace_pattern_editable,
            )
        )

        # Column view definition
        column_view: Gtk.ColumnView = build(
            Gtk.ColumnView
            + Properties(model=Gtk.NoSelection.new(self.__path_pairs_model))
        )
        column_view.append_column(
            Gtk.ColumnViewColumn.new(
                title="Picked paths",
                factory=self.__picked_paths_signal_factory,
            )
        )
        column_view.append_column(
            Gtk.ColumnViewColumn.new(
                title="Renamed paths",
                factory=self.__renamed_paths_signal_factory,
            )
        )

        # ---

        content = build(
            Adw.ToolbarView
            + TypedChild("top", header)
            + TypedChild(
                "content",
                Adw.ClampScrollable
                + Children(
                    Gtk.Box
                    + Properties(orientation=Gtk.Orientation.VERTICAL)
                    + Children(regex_section, column_view)
                ),
            )
        )

        # Assemble the page
        self.set_can_pop(True)
        self.set_tag(self.TAG)
        self.set_title("Rename")
        self.set_child(content)

    def __init__(self):
        super().__init__()
        self.__path_pairs_model = Gio.ListStore.new(item_type=PairOfStrings)

        # Factory and lifecycle manager for picked paths
        self.__picked_paths_signal_factory = Gtk.SignalListItemFactory()
        self.__picked_paths_lifecycle_manager = PathLifeCycleManager(
            displayed_property_name="first"
        )
        self.__picked_paths_lifecycle_manager.attach_to(
            self.__picked_paths_signal_factory
        )

        # Factory and lifecycle manager for renamed paths
        self.__renamed_paths_signal_factory = Gtk.SignalListItemFactory()
        self.__renamed_paths_lifecycle_manager = PathLifeCycleManager(
            displayed_property_name="second"
        )
        self.__renamed_paths_lifecycle_manager.attach_to(
            self.__renamed_paths_signal_factory
        )

        self.__build()

    def __on_regex_changed(self, editable: Gtk.Editable):
        self.activate_action(
            name=f"app.{ActionNames.REGEX}",
            args=GLib.Variant.new_string(editable.get_text()),
        )

    def __on_replace_pattern_changed(self, editable: Gtk.Editable):
        self.activate_action(
            name=f"app.{ActionNames.REPLACE_PATTERN}",
            args=GLib.Variant.new_string(editable.get_text()),
        )

    def __update_path_pairs_model(self) -> None:
        """Update the path pairs model based on the current rename target."""

        transform: callable[[str], str]
        match self.rename_target:
            case RenameTarget.FULL:
                transform = lambda path: path  # noqa: E731
            case RenameTarget.NAME:
                transform = lambda path: Path(path).name  # noqa: E731
            case RenameTarget.STEM:
                transform = lambda path: Path(path).stem  # noqa: E731
            case _:
                raise ValueError(f"Unknown rename target: {self.rename_target}")

        self.__path_pairs_model.remove_all()
        for picked, renamed in zip(self.__picked_paths, self.__renamed_paths):
            display_pair = PairOfStrings()
            display_pair.first = transform(picked)
            display_pair.second = transform(renamed)
            self.__path_pairs_model.append(display_pair)
