from gi.repository import Adw, GObject, Gtk

from main.widget_builder.widget_builder import (
    Children,
    Handlers,
    Properties,
    build,
)
from main.signals import Signals


class EmptyPage(Adw.NavigationPage):
    """Component for the empty page in the main window."""

    TAG = "empty-page"

    @GObject.Signal(name=Signals.PICK_FILES)
    def signal_pick_files(self):
        """Signal emitted when the user requests to pick files."""
        pass

    def __build(self) -> None:
        status_page = build(
            Adw.StatusPage
            + Properties(
                title="No files selected",
                description="Start renaming by first selecting files",
                icon_name="document-open-symbolic",
            )
            + Children(
                Gtk.Button
                + Properties(css_classes=["suggested-action", "pill"])
                + Handlers(clicked=self.__on_files_picker_requested)
                + Children(Gtk.Label + Properties(label="Select files to rename"))
            )
        )

        self.set_can_pop(False)
        self.set_title("Select Files")
        self.set_tag(self.TAG)
        self.set_child(status_page)

    def __init__(self):
        super().__init__()
        self.__build()

    def __on_files_picker_requested(self, _source) -> None:
        """Signal handler for the button click to pick files."""
        self.emit(Signals.PICK_FILES)
