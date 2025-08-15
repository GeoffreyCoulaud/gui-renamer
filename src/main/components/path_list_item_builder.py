from gi.repository import Gtk  # type: ignore

from main.widget_builder.widget_builder import Properties, build


class PathLifeCycleManager:
    """Class in charge of managing ListItem lifecycle for path widgets"""

    __displayed_property_name: str

    def __init__(self, displayed_property_name: str):
        self.__displayed_property_name = displayed_property_name

    def attach_to(self, signal_factory: Gtk.SignalListItemFactory):
        """Attach the builder to the factory's signals"""

        signal_factory.connect("setup", self.__on_setup)
        signal_factory.connect("bind", self.__on_bind)

    def __on_setup(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        widget = build(Gtk.Label + Properties(label="", wrap=True))
        item.set_child(widget)

    def __on_bind(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        pair = item.get_item()
        path = pair.get_property(self.__displayed_property_name)
        widget: Gtk.Label = item.get_child()
        widget.set_label(path)
