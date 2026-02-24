"""Implementation of NavigatorPort for presentation layer."""

from typing import Any

from tui_app.application.ports import NavigatorPort
from tui_app.presentation.messages import NavigateTo, PushScreen, PopScreen, ExitApp


class PresentationNavigator(NavigatorPort):
    """Implementation of NavigatorPort for the presentation layer."""

    def __init__(self, screen) -> None:
        self.screen = screen

    def navigate_to(self, screen_name: str, **kwargs: Any) -> None:
        self.screen.post_message(NavigateTo(screen_name, **kwargs))

    def push_modal(self, screen: Any) -> None:
        self.screen.post_message(PushScreen(screen))

    def pop_current_screen(self) -> None:
        self.screen.post_message(PopScreen())

    def exit_application(self) -> None:
        self.screen.post_message(ExitApp())
