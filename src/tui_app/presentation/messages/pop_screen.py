"""Message for requesting to pop the current screen from the stack."""

from textual.message import Message


class PopScreen(Message):
    """Message posted by screens to request popping the current screen."""
    pass
