from gi.repository import Gtk  # type: ignore


class PathListItemFactory:
    """Class in charge of list items for paths in the renaming page."""

    def attach_to(self, signal_factory: Gtk.SignalListItemFactory):
        signal_factory.connect("setup", self.__on_setup)
        signal_factory.connect("bind", self.__on_bind)
        signal_factory.connect("unbind", self.__on_unbind)
        signal_factory.connect("teardown", self.__on_teardown)

    @staticmethod
    def __on_setup(factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        pass

    @staticmethod
    def __on_bind(factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        pass

    @staticmethod
    def __on_unbind(factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        pass

    @staticmethod
    def __on_teardown(factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        pass
