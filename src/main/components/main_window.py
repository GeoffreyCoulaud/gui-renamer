from enum import StrEnum
from gi.repository import Adw, Gtk, GObject

from main.components.widget_builder.widget_builder import (
    Children,
    Handlers,
    TypedChild,
    build,
    Properties,
)
from main.signals import Signals


class PageTags(StrEnum):
    """Enum for the names of the pages in the main window."""

    EMPTY_PAGE = "empty-page"
    RENAMING_PAGE = "renaming-page"


class MainWindow(Adw.ApplicationWindow):
    """MVC view for the main window of the application."""

    @GObject.Signal(name=Signals.PICK_FILES)
    def signal_pick_files(self):
        pass

    @GObject.Signal(name=Signals.REGEX_CHANGED, arg_types=(str,))
    def signal_regex_changed(self, _regex_text: str):
        pass

    def __build_renaming_page(self) -> Adw.NavigationPage:
        margin = 12
        boxed_list_properties = Properties(
            css_classes=["boxed-list"],
            selection_mode=Gtk.SelectionMode.NONE,
        )

        # Regex section
        self.__regex_editable: Adw.EntryRow = build(
            Adw.EntryRow
            + Properties(title="Regex Pattern", css_classes=["monospace"])
            + Handlers(changed=self.__on_regex_changed)
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
            + Children(self.__regex_editable)
        )

        # Paths new path section
        self.__picked_paths = build(
            Gtk.ListBox
            + boxed_list_properties
            + Properties(
                margin_top=margin / 2,
                margin_bottom=margin,
                margin_start=margin,
                margin_end=margin / 2,
            )
        )
        self.__renamed_paths = build(
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
            + Children(self.__picked_paths, self.__renamed_paths)
        )

        return build(
            Adw.NavigationPage
            + Properties(can_pop=True, tag=PageTags.RENAMING_PAGE, title="Rename")
            + Children(
                Gtk.Box
                + Properties(orientation=Gtk.Orientation.VERTICAL)
                + Children(regex_section, paths_section)
            )
        )

    def __build_empty_page(self) -> Adw.NavigationPage:
        return build(
            Adw.NavigationPage
            + Properties(can_pop=False, tag=PageTags.EMPTY_PAGE, title="Select Files")
            + Children(
                Adw.StatusPage
                + Properties(
                    title="No files selected",
                    description="Start renaming by first selecting files",
                    icon_name="document-open-symbolic",
                )
                + Children(
                    Gtk.Button
                    + Properties(css_classes=["suggested-action"])
                    + Handlers(clicked=self.__on_files_picker_requested)
                    + Children(
                        Adw.ButtonContent
                        + Properties(
                            icon_name="document-open-symbolic",
                            label="Select files to rename",
                        )
                    )
                )
            )
        )

    def __build(self):
        header = Adw.HeaderBar + Children(Adw.WindowTitle + Properties(title="Renamer"))
        self.__navigation: Adw.NavigationView = build(
            Adw.NavigationView
            + Children(
                self.__build_empty_page(),
                self.__build_renaming_page(),
            )
        )
        self.set_content(
            build(
                Adw.ToolbarView
                + TypedChild(
                    "top",
                    header,
                )
                + TypedChild(
                    "content",
                    Adw.ClampScrollable + Children(self.__navigation),
                )
            )
        )
        self.set_default_size(800, 600)

    def __on_files_picker_requested(self, *args):
        self.emit(Signals.PICK_FILES)

    def __on_regex_changed(self, regex_text: str, *args):
        self.emit(Signals.REGEX_CHANGED, regex_text)

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()

    def update_picked_paths(self, paths: list[str]):
        """Update the picked paths list with the provided paths."""
        self.__picked_paths.remove_all()
        for path in paths:
            item = self.__build_path_widget(path)
            self.__picked_paths.append(item)
        if paths:
            self.__navigation.push_by_tag(PageTags.RENAMING_PAGE)
        else:
            self.__navigation.pop_to_tag(PageTags.EMPTY_PAGE)

    def update_renamed_paths(self, paths: list[str]):
        """Update the renamed paths list with the provided paths."""
        self.__renamed_paths.remove_all()
        for path in paths:
            item = self.__build_path_widget(path)
            self.__renamed_paths.append(item)

    def __build_path_widget(self, path: str) -> Gtk.ListBoxRow:
        # TODO better display of file paths, right now just a label
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
