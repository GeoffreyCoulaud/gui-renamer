from enum import StrEnum
from pathlib import Path
from gi.repository import Adw, GObject, Gtk

from main.widget_builder.widget_builder import (
    Children,
    Properties,
    OutboundProperty,
    TypedChild,
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
        NOTIFY_APPLY_TO_FULL_PATH = "notify::apply-to-full-path"
        PICK_FILES = "pick-files"

    # --- PyGobject things

    renamed_paths: list[str] = GObject.Property(type=object)
    picked_paths: list[str] = GObject.Property(type=object)
    regex = GObject.Property(type=str, default="")
    replace_pattern = GObject.Property(type=str, default="")
    apply_to_full_path: bool = GObject.Property(type=bool, default=False)

    # ---

    def __build(self):
        margin = 12
        BOXED_LIST_PROPERTIES = Properties(
            css_classes=["boxed-list"],
            selection_mode=Gtk.SelectionMode.NONE,
        )
        popover = build(
            Gtk.Popover
            + Children(
                Gtk.Box
                + Properties(orientation=Gtk.Orientation.VERTICAL)
                + Children(
                    # TODO add the settings here
                    Gtk.CheckButton
                    + Properties(
                        label="Apply to full path",
                        active=False,
                    )
                    + OutboundProperty(
                        source_property="active",
                        target=self,
                        target_property="apply-to-full-path",
                    )
                )
            )
        )
        menu_button = Gtk.MenuButton + Properties(
            icon_name="open-menu-symbolic",
            popover=popover,
        )
        header = (
            Adw.HeaderBar
            + Children(Adw.WindowTitle + Properties(title="Renamer"))
            + TypedChild("end", menu_button)
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
            + BOXED_LIST_PROPERTIES
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
            + BOXED_LIST_PROPERTIES
            + Properties(
                margin_top=margin / 2,
                margin_bottom=margin,
                margin_start=margin,
                margin_end=margin / 2,
            )
        )
        self.__renamed_paths_listbox: Gtk.ListBox = build(
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
            + Properties(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
            + Children(self.__picked_paths_listbox, self.__renamed_paths_listbox)
        )

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

        text = path if self.apply_to_full_path else Path(path).name

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
