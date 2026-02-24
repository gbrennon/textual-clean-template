from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static

from tui_app.presentation.screens.app_screen import AppScreen


class HomeScreen(AppScreen):
    """Home screen. Replace with your application's home screen."""

    BINDINGS = [Binding("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome. Replace this with your UI.", id="home-content")
        yield Footer()

    def action_quit(self) -> None:
        self.navigator.exit_application()
