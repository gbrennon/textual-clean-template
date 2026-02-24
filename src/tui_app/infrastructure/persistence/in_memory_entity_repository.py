from tui_app.domain.entities.entity import Entity


class InMemoryEntityRepository:
    """In-memory adapter implementing EntityRepository. Replace with your persistence adapter."""

    def __init__(self) -> None:
        self._store: dict[str, Entity] = {}

    async def save(self, entity: Entity) -> None:
        raise NotImplementedError

    async def find_by_id(self, entity_id: str) -> Entity | None:
        raise NotImplementedError

    async def find_all(self) -> list[Entity]:
        raise NotImplementedError

    async def delete(self, entity_id: str) -> None:
        raise NotImplementedError
