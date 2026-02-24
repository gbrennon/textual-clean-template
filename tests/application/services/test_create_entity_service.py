import pytest

from tui_app.application.ports.create_entity_port import CreateEntityRequest
from tui_app.application.services.create_entity_service import CreateEntityService


class FakeEntityRepository:
    def __init__(self) -> None:
        self._store: list = []

    async def save(self, entity) -> None:
        self._store.append(entity)

    async def find_by_id(self, entity_id: str):
        return None

    async def find_all(self):
        return list(self._store)

    async def delete(self, entity_id: str) -> None:
        pass


@pytest.mark.asyncio
async def test_create_entity_service_execute_raises_not_implemented() -> None:
    repository = FakeEntityRepository()
    service = CreateEntityService(repository)
    with pytest.raises(NotImplementedError):
        await service.execute(CreateEntityRequest(name="Test"))
