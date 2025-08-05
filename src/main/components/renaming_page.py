from gi.repository import Adw, Gtk, GObject

from main.components.widget_builder.widget_builder import (
    Children,
    Handlers,
    Properties,
    build,
)
from main.signals.signals import Signals


class RenamingPage(Adw.NavigationPage):
    """A page to display the renaming interface"""

    @GObject.Signal(name=Signals.REGEX_CHANGED, arg_types=(str,))
    def regex_changed(self, _regex_text: str):
        """Signal emitted when the regex changes."""

    def __build(self):
        # Regex section
        self.__regex_editable: Adw.EntryRow = build(
            Adw.EntryRow
            + Properties(title="Regex Pattern")
            + Handlers(changed=self.__on_regex_changed)
        )
        regex_section = build(Gtk.ListBox + Children(self.__regex_editable))

        # Paths new path section
        self.__current_paths = build(Gtk.ListBox)
        self.__new_paths = build(Gtk.ListBox)
        paths_section = build(
            Gtk.Box
            + Properties(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
            + Children(self.__current_paths, self.__new_paths)
        )

        # Vertical box to hold the regex section, plus the paths new path section
        vertical_box = build(
            Gtk.Box
            + Properties(orientation=Gtk.Orientation.VERTICAL)
            + Children(regex_section, paths_section)
        )

        self.set_child(vertical_box)

    def __init__(self):
        super().__init__()
        self.__build()

    def __on_regex_changed(self, _source_object):
        regex_text = self.__regex_editable.get_text()
        self.emit(Signals.REGEX_CHANGED, regex_text)

    def update_picked_paths(self, paths: list[str]):
        """Update the new paths list with the provided paths."""
        self.__current_paths.remove_all()
        for path in paths:
            label = build(
                Gtk.Label
                + Properties(
                    label=path,
                    hexpand=True,
                    justify=Gtk.Justification.LEFT,
                )
            )
            self.__current_paths.append(label)

    def update_renamed_paths(self, paths: list[str]):
        """Update the new paths list with the provided paths."""
        self.__new_paths.remove_all()
        for path in paths:
            label = build(
                Gtk.Label
                + Properties(
                    label=path,
                    hexpand=True,
                    justify=Gtk.Justification.LEFT,
                )
            )
            self.__new_paths.append(label)
