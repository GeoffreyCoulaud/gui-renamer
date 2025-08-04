from main.components.main_window import MainWindow
from main.models.main_model import MainModel


class MainWindowController:
    """MVC controller for the main window of the application."""

    def __init__(self, model: MainModel, view: MainWindow):
        self.__model = model
        self.__view = view

    def present(self):
        """Present the main window"""
        self.__view.present()
