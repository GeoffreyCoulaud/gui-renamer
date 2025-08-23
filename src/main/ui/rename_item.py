from gi.repository import GObject, Gtk, Pango  # type: ignore

from main.types.mistakes import RenameDestinationMistake
from main.ui.widget_builder.widget_builder import (
    Children,
    InboundProperty,
    Properties,
    build,
)


class RenameItemData(GObject.GObject):
    """Data object for rename item widget"""

    picked_path: str = GObject.Property(type=str)  # type: ignore
    renamed_path: str = GObject.Property(type=str)  # type: ignore
    index: int = GObject.Property(type=int, default=0)  # type: ignore
    count: int = GObject.Property(type=int, default=0)  # type: ignore
    mistake: RenameDestinationMistake | None = GObject.Property(type=object)  # type: ignore

    def __init__(
        self,
        picked_path: str,
        renamed_path: str,
        index: int,
        count: int,
        mistake: RenameDestinationMistake | None = None,
    ) -> None:
        super().__init__()
        self.picked_path = picked_path
        self.renamed_path = renamed_path
        self.index = index
        self.count = count
        self.mistake = mistake


class RenameItemWidget(Gtk.CenterBox):
    """Rename item widget"""

    MARGIN: int = 12

    # --- Inbound properties

    __index: int = 0

    @GObject.Property(type=int, default=0)
    def index(self) -> int:
        return self.__index

    @index.setter
    def index_setter(self, value: int) -> None:
        self.__index = value
        self.__update_index_appearance()

    __count: int = 0

    @GObject.Property(type=int, default=0)
    def count(self) -> int:
        return self.__count

    @count.setter
    def count_setter(self, value: int) -> None:
        self.__count = value
        self.__update_index_appearance()

    __mistake: RenameDestinationMistake | None = None

    @GObject.Property(type=object)
    def mistake(self) -> RenameDestinationMistake | None:
        return self.__mistake

    @mistake.setter
    def mistake_setter(self, value: RenameDestinationMistake | None) -> None:
        self.__mistake = value
        if value:
            self.add_css_class("error")
        else:
            self.remove_css_class("error")

    picked_path = GObject.Property(type=str, default="")
    renamed_path = GObject.Property(type=str, default="")

    # ---

    __picked_label: Gtk.Label
    __renamed_label: Gtk.Label
    __separator: Gtk.Label

    def __wrap_label_for_sizing(self, widget: Gtk.Widget) -> Gtk.Widget:
        return build(
            Gtk.ScrolledWindow
            + Properties(
                hscrollbar_policy=Gtk.PolicyType.NEVER,
                vscrollbar_policy=Gtk.PolicyType.NEVER,
            )
            + Children(widget)
        )

    def __build(self) -> None:
        label_props = Properties(
            wrap=True,
            wrap_mode=Pango.WrapMode.WORD_CHAR,
            xalign=0.0,
            hexpand=True,
            ellipsize=Pango.EllipsizeMode.NONE,
        )

        self.__picked_label = build(
            Gtk.Label
            + label_props
            + Properties(
                margin_start=self.MARGIN,
                margin_end=self.MARGIN / 2,
                valign=Gtk.Align.START,
                selectable=True,
            )
            + InboundProperty(
                source=self,
                source_property="picked-path",
                target_property="label",
            )
        )

        self.__renamed_label = build(
            Gtk.Label
            + label_props
            + Properties(
                margin_start=self.MARGIN / 2,
                margin_end=self.MARGIN,
                valign=Gtk.Align.START,
            )
            + InboundProperty(
                source=self,
                source_property="renamed-path",
                target_property="label",
            )
        )

        self.__separator = build(
            Gtk.Label
            + Properties(
                label="→",
                margin_start=self.MARGIN / 2,
                margin_end=self.MARGIN / 2,
                valign=Gtk.Align.START,
                hexpand=False,
            )
        )

        self.set_start_widget(self.__wrap_label_for_sizing(self.__picked_label))
        self.set_center_widget(self.__separator)
        self.set_end_widget(self.__wrap_label_for_sizing(self.__renamed_label))

        if self.__mistake:
            self.add_css_class("error")

    def __update_index_appearance(self) -> None:
        """Update the label's display based on the item's index"""

        is_first = self.index == 0
        top_margin = int(self.MARGIN / (1 if is_first else 2))
        self.__picked_label.set_margin_top(top_margin)
        self.__renamed_label.set_margin_top(top_margin)
        self.__separator.set_margin_top(top_margin)

        is_last = self.index == (self.count - 1)
        bottom_margin = int(self.MARGIN / (1 if is_last else 2))
        self.__picked_label.set_margin_bottom(bottom_margin)
        self.__renamed_label.set_margin_bottom(bottom_margin)
        self.__separator.set_margin_bottom(bottom_margin)

        # TODO set a class to alternate the background color for lisibility

    def __init__(self) -> None:
        super().__init__()
        self.set_css_name("rename-item")
        self.__build()


class RenameItemLifeCycleManager:
    """Class in charge of managing ListItem lifecycle for path widgets"""

    def attach_to(self, signal_factory: Gtk.SignalListItemFactory):
        """Attach the builder to the factory's signals"""
        signal_factory.connect("bind", self.__on_bind)
        signal_factory.connect("setup", self.__on_setup)

    def __on_setup(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        item.set_child(RenameItemWidget())

    def __on_bind(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        widget: RenameItemWidget = item.get_child()  # type: ignore
        data: RenameItemData = item.get_item()  # type: ignore

        widget.picked_path = data.picked_path
        widget.renamed_path = data.renamed_path
        widget.index = data.index
        widget.count = data.count
        widget.mistake = data.mistake
