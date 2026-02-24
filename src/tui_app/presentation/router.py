from enum import StrEnum


class ScreenName(StrEnum):
    """Enumeration of all screens. Add your screen names here."""

    HOME = "home"


class Router:
    """Central navigation router."""

    def __init__(self, app, navigator) -> None:
        self.app = app
        self.navigator = navigator
        self._registry: dict[ScreenName, type] = {}

    def register_screen(self, name: ScreenName, screen_class: type) -> None:
        self._registry[name] = screen_class

    def push_screen(self, screen_name: ScreenName, **kwargs) -> None:
        if screen_name not in self._registry:
            raise ValueError(f"Unknown screen: {screen_name}")
        screen_class = self._registry[screen_name]
        self.app.push_screen(screen_class(navigator=self.navigator, **kwargs))

    def pop_screen(self) -> None:
        self.app.pop_screen()
