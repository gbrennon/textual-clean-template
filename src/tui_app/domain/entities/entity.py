from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entity:
    """Base domain entity. Replace with your domain aggregate root."""

    name: str
    entity_id: str | None = None
