from gi.repository import Adw, Gtk  # type: ignore

from main.models.action_names import ActionNames
from main.widget_builder.widget_builder import (
    Children,
    Properties,
    TypedChild,
    build,
)


class RenamedPage(Adw.NavigationPage):
    """Component to display a page when files have been renamed."""

    TAG = "renamed-page"

    def __build(self) -> None:
        header = Adw.HeaderBar + Children(Adw.WindowTitle + Properties(title="Renamed"))
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
                    title="Files Renamed",
                    description="You may undo the renaming or select new files to rename.",
                    icon_name="checkmark-symbolic",
                )
                + Children(
                    Gtk.Box
                    + Properties(spacing=12, halign=Gtk.Align.CENTER)
                    + Children(
                        Gtk.Button
                        + Properties(
                            css_classes=["pill"],
                            action_name=f"app.{ActionNames.UNDO_RENAMING}",
                            label="Undo renaming",
                        ),
                        Gtk.Button
                        + Properties(
                            css_classes=["suggested-action", "pill"],
                            action_name=f"app.{ActionNames.PICK_FILES}",
                            label="Select new files",
                        ),
                    )
                )
            )
        )

        self.set_can_pop(False)
        self.set_title("Renamed")
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
