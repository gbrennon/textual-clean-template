from tui_app.domain.entities.entity import Entity


def test_entity_has_name() -> None:
    entity = Entity(name="test")
    assert entity.name == "test"
