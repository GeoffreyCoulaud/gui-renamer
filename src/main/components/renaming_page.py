from enum import StrEnum
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

    class Signals(StrEnum):
        NOTIFY_PICKED_PATHS = "notify::picked-paths"
        NOTIFY_RENAMED_PATHS = "notify::renamed-paths"
        NOTIFY_REGEX = "notify::regex"
        NOTIFY_REPLACE_PATTERN = "notify::replace-pattern"
        PICK_FILES = "pick-files"

    # --- PyGobject things

    renamed_paths: list[str] = GObject.Property(type=object)
    picked_paths: list[str] = GObject.Property(type=object)
    regex = GObject.Property(type=str, default="")
    replace_pattern = GObject.Property(type=str, default="")

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
            )
        )
        self.__replace_pattern_editable: Adw.EntryRow = build(
            Adw.EntryRow
            + Properties(title="Replace Pattern", css_classes=["monospace"])
            + OutboundProperty(
                source_property="text",
                target=self,
                target_property="replace-pattern",
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
        self.connect(self.Signals.NOTIFY_PICKED_PATHS, self.__on_picked_paths_change)
        self.connect(self.Signals.NOTIFY_RENAMED_PATHS, self.__on_renamed_paths_change)

    def __on_picked_paths_change(self, *_args):
        self.__picked_paths_listbox.remove_all()
        for path in self.picked_paths:
            item = self.__build_path_widget(path)
            self.__picked_paths_listbox.append(item)

    def __on_renamed_paths_change(self, *_args):
        self.__renamed_paths_listbox.remove_all()
        for path in self.renamed_paths:
            item = self.__build_path_widget(path)
            self.__renamed_paths_listbox.append(item)

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
