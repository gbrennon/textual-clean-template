from tui_app.application.ports.create_entity_port import CreateEntityRequest, CreateEntityResponse
from tui_app.application.ports.entity_repository import EntityRepository


class CreateEntityService:
    def __init__(self, repository: EntityRepository) -> None:
        self._repository = repository

    async def execute(self, request: CreateEntityRequest) -> CreateEntityResponse:
        raise NotImplementedError
