"""Message for requesting to push a modal or screen onto the stack."""

from textual.message import Message


class PushScreen(Message):
    """Message posted by screens to request pushing a modal/screen.
    
    Attributes:
        screen: The screen instance to push onto the stack
    """
    
    def __init__(self, screen) -> None:
        super().__init__()
        self.screen = screen
