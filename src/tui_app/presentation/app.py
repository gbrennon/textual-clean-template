from pathlib import Path

from textual.app import App

from tui_app.infrastructure.container import Container
from tui_app.presentation.messages import ExitApp, NavigateTo, PopScreen, PushScreen
from tui_app.presentation.navigation.navigator import PresentationNavigator
from tui_app.presentation.router import Router, ScreenName
from tui_app.presentation.screens.home_screen import HomeScreen


class AppNavigator(PresentationNavigator):
    """Navigator that posts messages from the app level."""

    def __init__(self, app: App) -> None:
        self.screen = app


class TuiApp(App):
    """Main Textual application. Rename and extend for your domain."""

    CSS_PATH = [Path(__file__).parent / "css/app.tcss"]
    TITLE = "TUI App"

    def __init__(self, container: Container) -> None:
        super().__init__()
        self._container = container
        self.router: Router | None = None
        self.navigator: AppNavigator | None = None

    def on_mount(self) -> None:
        self.navigator = AppNavigator(self)
        self.router = Router(self, self.navigator)
        self.router.register_screen(ScreenName.HOME, HomeScreen)
        self.push_screen(HomeScreen(navigator=self.navigator))

    def on_navigate_to(self, message: NavigateTo) -> None:
        if self.router is not None:
            self.router.push_screen(message.screen_name, **message.kwargs)

    def on_pop_screen(self, message: PopScreen) -> None:
        self.pop_screen()

    def on_push_screen(self, message: PushScreen) -> None:
        self.push_screen(message.screen)

    def on_exit_app(self, message: ExitApp) -> None:
        self.exit()
