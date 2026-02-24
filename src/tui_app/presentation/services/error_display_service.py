"""Service for displaying form validation errors."""

from typing import Protocol

from textual.widgets import Static


class ErrorDisplayPort(Protocol):
    """Port for services that display form errors."""

    def show_error(self, error_widget: Static, message: str) -> None: ...
    def clear_error(self, error_widget: Static) -> None: ...


class ErrorDisplayService:
    """Service for displaying form validation errors."""

    def show_error(self, error_widget: Static, message: str) -> None:
        error_widget.update(f"[red]{message}[/red]")

    def clear_error(self, error_widget: Static) -> None:
        error_widget.update("")
