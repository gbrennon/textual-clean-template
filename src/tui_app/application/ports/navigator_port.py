"""Port for navigation control - owned by application layer."""

from typing import Any, Protocol


class NavigatorPort(Protocol):
    """Port for requesting navigation between screens.

    This is an outbound port owned by the application layer. Screens
    depend on a PresentationNavigator implementation (in presentation) that
    implements this port.

    Navigation is an application concern because it represents state
    transitions that may have business logic implications.
    """

    def navigate_to(self, screen_name: str, **kwargs: Any) -> None:
        """Request navigation to another screen."""
        ...

    def push_modal(self, screen: Any) -> None:
        """Request to push a modal screen onto the stack."""
        ...

    def pop_current_screen(self) -> None:
        """Request to pop the current screen from the stack."""
        ...

    def exit_application(self) -> None:
        """Request to exit the entire application."""
        ...
