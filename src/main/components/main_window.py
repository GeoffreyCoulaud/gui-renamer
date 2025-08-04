from gi.repository import Adw, Gtk

from main.components.widget_builder.widget_builder import (
    TypedChild,
    build,
    Properties,
)


class MainWindow(Adw.ApplicationWindow):
    """MVC view for the main window of the application."""

    def __build(self):
        """Build the main window layout"""

        # Build the title bar
        title = build(Adw.WindowTitle + Properties(title="Renamer"))
        header_bar = build(Adw.HeaderBar + Properties(title_widget=title))
        content_area = build(Gtk.Box + Properties(orientation=Gtk.Orientation.VERTICAL))
        self.set_content(
            build(
                Adw.ToolbarView
                + TypedChild("top", header_bar)
                + TypedChild("content", content_area)
            )
        )
        self.set_default_size(800, 600)

    def __init__(self, application: Adw.Application):
        super().__init__(application=application)
        self.__build()
