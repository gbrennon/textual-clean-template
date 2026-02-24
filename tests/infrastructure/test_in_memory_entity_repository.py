import pytest

from tui_app.domain.entities.entity import Entity
from tui_app.infrastructure.persistence.in_memory_entity_repository import InMemoryEntityRepository


@pytest.mark.asyncio
async def test_save_raises_not_implemented() -> None:
    repo = InMemoryEntityRepository()
    with pytest.raises(NotImplementedError):
        await repo.save(Entity(name="test"))
