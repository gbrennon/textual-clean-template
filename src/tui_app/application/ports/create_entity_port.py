from dataclasses import dataclass
from typing import Protocol

from tui_app.domain.entities.entity import Entity


@dataclass(frozen=True)
class CreateEntityRequest:
    name: str


@dataclass(frozen=True)
class CreateEntityResponse:
    success: bool
    message: str
    entity: Entity | None = None


class CreateEntityPort(Protocol):
    async def execute(self, request: CreateEntityRequest) -> CreateEntityResponse: ...
