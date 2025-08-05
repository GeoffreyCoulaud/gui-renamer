from gi.repository import Adw, Gtk, GObject

from main.components.widget_builder.widget_builder import (
    Children,
    Handlers,
    Properties,
    build,
)
from main.signals.signals import Signals


class EmptyPage(Adw.NavigationPage):
    """A page to display when no files are selected"""

    @GObject.Signal(name=Signals.FILES_PICKER_REQUESTED)
    def files_picker_requested(self):
        """Signal emitted when the file picker button is clicked."""

    def __build(self):
        status = build(
            Adw.StatusPage
            + Properties(
                title="No files selected",
                description="Start renaming by first selecting files",
                icon_name="document-open-symbolic",
            )
            + Children(
                Gtk.Button
                + Properties(css_classes=[".suggested-action"])
                + Handlers(clicked=self.__on_button_clicked)
                + Children(
                    Adw.ButtonContent
                    + Properties(
                        icon_name="document-open-symbolic",
                        label="Select files to rename",
                    )
                )
            )
        )
        self.set_child(status)

    def __on_button_clicked(self, _source_object):
        """Handle the button click to request file selection."""
        self.emit(Signals.FILES_PICKER_REQUESTED)

    def __init__(self):
        super().__init__()
