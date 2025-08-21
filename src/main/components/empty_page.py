from gi.repository import Adw, Gtk  # type: ignore

from main.models.action_names import ActionNames
from main.widget_builder.widget_builder import (
    Children,
    Properties,
    TypedChild,
    build,
)


class EmptyPage(Adw.NavigationPage):
    """Component for the empty page in the main window."""

    TAG = "empty-page"

    def __build(self) -> None:
        header = Adw.HeaderBar + Children(Adw.WindowTitle + Properties(title="Renamer"))
        content = build(
            Adw.Clamp
            + Properties(
                margin_top=12,
                margin_bottom=12,
                margin_start=12,
                margin_end=12,
            )
            + Children(
                Adw.StatusPage
                + Properties(
                    title="No files selected",
                    description="Start renaming by first selecting files",
                    icon_name="document-open-symbolic",
                )
                + Children(
                    Gtk.Button
                    + Properties(
                        css_classes=["suggested-action", "pill"],
                        action_name=f"app.{ActionNames.PICK_FILES}",
                    )
                    + Children(Gtk.Label + Properties(label="Select files to rename"))
                )
            )
        )

        self.set_can_pop(False)
        self.set_title("Select Files")
        self.set_tag(self.TAG)
        self.set_child(
            build(
                Adw.ToolbarView
                + TypedChild("top", header)
                + TypedChild("content", content)
            )
        )

    def __init__(self):
        super().__init__()
        self.__build()
