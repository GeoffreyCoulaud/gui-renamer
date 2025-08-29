from gi.repository import Adw, Gtk  # type: ignore

from pattern_renamer.main.types.action_names import ActionNames
from pattern_renamer.main.ui.widget_builder.widget_builder import (
    Children,
    Properties,
    TypedChild,
    build,
)


class RenamedPage(Adw.NavigationPage):
    """Component to display a page when files have been renamed."""

    TAG = "renamed-page"

    def __build(self) -> None:
        header = Adw.HeaderBar + Children(
            Adw.WindowTitle + Properties(title=_("Renamed"))
        )
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
                    title=_("Files Renamed"),
                    description=_(
                        "You may undo the renaming or select new files to rename."
                    ),
                    icon_name="checkmark-symbolic",
                    css_classes=["success"],
                )
                + Children(
                    Gtk.Box
                    + Properties(spacing=12, halign=Gtk.Align.CENTER)
                    + Children(
                        Gtk.Button
                        + Properties(
                            css_classes=["pill"],
                            action_name=f"app.{ActionNames.UNDO_RENAMING}",
                            label=_("Undo renaming"),
                        ),
                        Gtk.Button
                        + Properties(
                            css_classes=["suggested-action", "pill"],
                            action_name=f"app.{ActionNames.PICK_FILES}",
                            label=_("Select new files"),
                        ),
                    )
                )
            )
        )

        self.set_can_pop(False)
        self.set_title(_("Renamed"))
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
