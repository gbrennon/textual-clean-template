from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class ConfirmDialog(ModalScreen):
    """A modal dialog for confirmation, centered and modal."""

    def __init__(self, message: str, on_confirm=None):
        super().__init__()
        self.message = message
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.message, id="confirm-message"),
            Horizontal(
                Button("Yes", variant="primary", id="confirm-yes"),
                Button("No", variant="default", id="confirm-no"),
                id="confirm-buttons"
            ),
            Static("[Enter] Yes    [Esc] No", id="confirm-hint"),
            id="confirm-dialog"
        )

    @on(Button.Pressed, "#confirm-yes")
    def handle_yes(self) -> None:
        if self.on_confirm:
            self.on_confirm()
        self.dismiss(True)

    @on(Button.Pressed, "#confirm-no")
    def handle_no(self) -> None:
        self.dismiss(False)
