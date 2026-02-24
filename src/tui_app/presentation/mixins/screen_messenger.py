"""Mixin for screens to post messages without direct framework access."""

from textual.screen import Screen

from tui_app.presentation.messages import NavigateTo, PopScreen, PushScreen, ExitApp


class ScreenMessenger:
    """Mixin that provides message-posting convenience methods for screens."""

    def navigate_to(self, screen_name: str, **kwargs) -> None:
        self.post_message(NavigateTo(screen_name, **kwargs))

    def push_modal(self, screen: Screen) -> None:
        self.post_message(PushScreen(screen))

    def pop_current_screen(self) -> None:
        self.post_message(PopScreen())

    def exit_application(self) -> None:
        self.post_message(ExitApp())
