"""Message for requesting navigation to another screen."""

from textual.message import Message


class NavigateTo(Message):
    """Message posted by screens to request navigation to another screen.
    
    Attributes:
        screen_name: Name of the target screen to navigate to
        kwargs: Optional arguments to pass to the target screen
    """
    
    def __init__(self, screen_name: str, **kwargs) -> None:
        super().__init__()
        self.screen_name = screen_name
        self.kwargs = kwargs
