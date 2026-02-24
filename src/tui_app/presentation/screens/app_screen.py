"""Base screen for all application screens."""

from textual.screen import Screen

from tui_app.application.ports import NavigatorPort


class AppScreen(Screen):
    """Base screen for all application screens."""

    def __init__(self, navigator: NavigatorPort, **kwargs):
        super().__init__(**kwargs)
        self.navigator = navigator
