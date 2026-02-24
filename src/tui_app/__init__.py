from tui_app.presentation.app import TuiApp


def main() -> None:
    """Entry point."""
    from tui_app.infrastructure.container import Container
    container = Container()
    app = TuiApp(container=container)
    app.run()


__all__ = ["TuiApp", "main"]
