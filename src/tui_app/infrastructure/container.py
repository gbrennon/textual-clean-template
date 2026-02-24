from tui_app.application.ports.entity_repository import EntityRepository
from tui_app.application.services.create_entity_service import CreateEntityService
from tui_app.infrastructure.persistence.in_memory_entity_repository import InMemoryEntityRepository


class Container:
    """Composition root. Wire all dependencies here."""

    def __init__(self) -> None:
        repository: EntityRepository = InMemoryEntityRepository()
        self.create_entity_service = CreateEntityService(repository)
