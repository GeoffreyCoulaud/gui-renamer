from gi.repository import Gtk, Pango  # type: ignore

from main.components.pair_of_strings import PairOfStrings
from main.widget_builder.widget_builder import Children, Properties, build


class PathPairLifeCycleManager:
    """Class in charge of managing ListItem lifecycle for path widgets"""

    def attach_to(self, signal_factory: Gtk.SignalListItemFactory):
        """Attach the builder to the factory's signals"""
        signal_factory.connect("bind", self.__on_bind)

    def __on_bind(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem):
        pair: PairOfStrings = item.get_item()
        margin = 12
        label_props = Properties(
            wrap=True,
            xalign=0.0,
            hexpand=True,
            ellipsize=Pango.EllipsizeMode.NONE,
            margin_top=margin if pair.is_first else margin / 2,
            margin_bottom=margin if pair.is_last else margin / 2,
        )

        # TODO add custom CSS to the widget to alternate background colors
        # (As tables do to ease reading)

        item.set_child(
            build(
                Gtk.Box
                + Properties(homogeneous=True)
                + Children(
                    Gtk.Label
                    + Properties(
                        label=pair.first,
                        margin_start=margin,
                        margin_end=margin / 2,
                        valign=Gtk.Align.START,
                    )
                    + label_props,
                    Gtk.Label
                    + Properties(
                        label=pair.second,
                        margin_start=margin / 2,
                        margin_end=margin,
                        valign=Gtk.Align.START,
                    )
                    + label_props,
                )
            )
        )
