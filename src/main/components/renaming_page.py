import logging
from gi.repository import Adw, GObject, Gtk

from main.widget_builder.widget_builder import (
    Children,
    Properties,
    OutboundProperty,
    build,
)


class RenamingPage(Adw.NavigationPage):
    """Component for the renaming page of the application."""

    TAG = "renaming-page"

    # --- PyGobject things

    __picked_paths: list[str]

    @GObject.Property(type=object)
    def picked_paths(self) -> list[str]:
        return self.__picked_paths

    @picked_paths.setter
    def picked_paths(self, paths: list[str]):
        self.__picked_paths = paths
        self.__picked_paths_listbox.remove_all()
        for path in paths:
            logging.debug(f"Adding picked path: {path}")
            item = self.__build_path_widget(path)
            self.__picked_paths_listbox.append(item)

    __renamed_paths: list[str]

    @GObject.Property(type=object)
    def renamed_paths(self) -> list[str]:
        return self.__renamed_paths

    @renamed_paths.setter
    def renamed_paths(self, paths: list[str]):
        self.__renamed_paths = paths
        for path in paths:
            logging.debug(f"Adding renamed path: {path}")
            item = self.__build_path_widget(path)
            self.__renamed_paths_listbox.append(item)

    __regex: str

    @GObject.Property(type=str)
    def regex(self) -> str:
        return self.__regex

    @regex.setter
    def regex(self, pattern: str):
        self.__regex = pattern

    __replace_pattern: str

    @GObject.Property(type=str)
    def replace_pattern(self) -> str:
        return self.__replace_pattern

    @replace_pattern.setter
    def replace_pattern(self, pattern: str):
        self.__replace_pattern = pattern

    # ---

    def __build(self):
        margin = 12
        boxed_list_properties = Properties(
            css_classes=["boxed-list"],
            selection_mode=Gtk.SelectionMode.NONE,
        )

        # Regex section
        self.__regex_editable: Adw.EntryRow = build(
            Adw.EntryRow
            + Properties(title="Regex Pattern", css_classes=["monospace"])
            + OutboundProperty(
                source_property="text",
                target=self,
                target_property="regex",
                flags=GObject.BindingFlags.SYNC_CREATE,
            )
        )
        self.__replace_pattern_editable: Adw.EntryRow = build(
            Adw.EntryRow
            + Properties(title="Replace Pattern", css_classes=["monospace"])
            + OutboundProperty(
                source_property="text",
                target=self,
                target_property="replace-pattern",
                flags=GObject.BindingFlags.SYNC_CREATE,
            )
        )
        regex_section = build(
            Gtk.ListBox
            + boxed_list_properties
            + Properties(
                margin_top=margin,
                margin_bottom=margin / 2,
                margin_start=margin,
                margin_end=margin,
            )
            + Children(
                self.__regex_editable,
                self.__replace_pattern_editable,
            )
        )

        # Paths new path section
        self.__picked_paths_listbox: Gtk.ListBox = build(
            Gtk.ListBox
            + boxed_list_properties
            + Properties(
                margin_top=margin / 2,
                margin_bottom=margin,
                margin_start=margin,
                margin_end=margin / 2,
            )
        )
        self.__renamed_paths_listbox: Gtk.ListBox = build(
            Gtk.ListBox
            + boxed_list_properties
            + Properties(
                margin_top=margin / 2,
                margin_bottom=margin,
                margin_start=margin / 2,
                margin_end=margin,
            )
        )
        paths_section = build(
            Gtk.Box
            + Properties(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
            + Children(self.__picked_paths_listbox, self.__renamed_paths_listbox)
        )

        # Assemble the page
        box = build(
            Gtk.Box
            + Properties(orientation=Gtk.Orientation.VERTICAL)
            + Children(regex_section, paths_section)
        )
        self.set_can_pop(True)
        self.set_tag(self.TAG)
        self.set_title("Rename")
        self.set_child(box)

    def __init__(self):
        super().__init__()
        self.__build()

    def __build_path_widget(self, path: str) -> Gtk.ListBoxRow:
        margin = 8
        return build(
            Gtk.ListBoxRow
            + Children(
                Gtk.Label
                + Properties(
                    label=path,
                    css_classes=["monospace"],
                    justify=Gtk.Justification.LEFT,
                    margin_bottom=margin,
                    margin_top=margin,
                    margin_start=margin,
                    margin_end=margin,
                )
            )
        )
