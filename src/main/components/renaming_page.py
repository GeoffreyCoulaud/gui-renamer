from pathlib import Path

from gi.repository import Adw, Gio, GLib, GObject, Gtk  # type: ignore

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

    __picked_file_paths: list[str]

    @GObject.Property(type=object)
    def picked_file_paths(self):
        return self.__picked_file_paths

    @picked_file_paths.setter
    def picked_file_paths_setter(self, value: list[str]):
        self.__picked_file_paths = value
        self.__picked_paths_listbox.remove_all()
        for path in self.__picked_file_paths:
            item = self.__build_path_widget(path)
            self.__picked_paths_listbox.append(item)

    __renamed_file_paths: list[str]

    @GObject.Property(type=object)
    def renamed_file_paths(self):
        return self.__renamed_file_paths

    @renamed_file_paths.setter
    def renamed_file_paths_setter(self, value: list[str]):
        self.__renamed_file_paths = value
        self.__renamed_paths_listbox.remove_all()
        for path in self.__renamed_file_paths:
            item = self.__build_path_widget(path)
            self.__renamed_paths_listbox.append(item)

    rename_target: RenameTarget = GObject.Property(type=str)

    # ---

    __paths_model: Gio.ListModel

    # TODO remove
    __picked_paths_listbox: Gtk.ListBox
    __renamed_paths_listbox: Gtk.ListBox

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

        # Paths new path section
        # TODO Replace with a grid, to have word wrap and coherent lines.

        self.__picked_paths_listbox = build(
            Gtk.ListBox
            + BOXED_LIST_PROPERTIES
            + Properties(
                margin_top=margin / 2,
                margin_bottom=margin,
                margin_start=margin,
                margin_end=margin / 2,
            )
        )
        self.__renamed_paths_listbox = build(
            Gtk.ListBox
            + BOXED_LIST_PROPERTIES
            + Properties(
                margin_top=margin / 2,
                margin_bottom=margin,
                margin_start=margin / 2,
                margin_end=margin,
            )
        )
        paths_section = build(
            Gtk.Box
            + Properties(orientation=Gtk.Orientation.HORIZONTAL)
            + Children(self.__picked_paths_listbox, self.__renamed_paths_listbox)
        )

        # New column view to display the paths
        column_view = Gtk.ColumnView()
        signal_factory = Gtk.SignalListItemFactory()
        column_view.append_column(
            Gtk.ColumnViewColumn.new(
                title="Picked paths",
                factory=signal_factory,
            )
        )
        column_view.append_column(
            Gtk.ColumnViewColumn.new(
                title="Renamed paths",
                factory=signal_factory,
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
                    + Children(regex_section, paths_section)
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
        self.__path_widget_factory = Gtk.SignalListItemFactory()
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

    def __build_path_widget(self, path: str) -> Gtk.ListBoxRow:
        text: str
        match self.rename_target:
            case RenameTarget.FULL:
                text = path
            case RenameTarget.NAME:
                text = Path(path).name
            case RenameTarget.STEM:
                text = Path(path).stem
            case _:
                TypeError(f"Unknown rename target: {self.rename_target}")

        margin = 8

        # TODO replace with a grid item
        return build(
            Gtk.ListBoxRow
            + Children(
                Gtk.Label
                + Properties(
                    label=text,
                    css_classes=["monospace"],
                    justify=Gtk.Justification.LEFT,
                    margin_bottom=margin,
                    margin_top=margin,
                    margin_start=margin,
                    margin_end=margin,
                )
            )
        )
