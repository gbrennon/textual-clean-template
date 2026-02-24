"""Message for requesting application exit."""

from textual.message import Message


class ExitApp(Message):
    """Message posted by screens to request application exit."""
    pass
