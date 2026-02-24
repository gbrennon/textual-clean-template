---
applyTo: "**/*.py"
---

# Clean / Hexagonal Architecture

This project follows Hexagonal Architecture (Ports & Adapters). These concepts are language-agnostic; examples below show the Python implementation.

# Clean / Hexagonal Architecture

This project follows Hexagonal Architecture (Ports & Adapters). These concepts are language-agnostic; examples below show the Python implementation.

## Conceptual Layers

There are four conceptual layers, from innermost to outermost:

| Layer | Responsibility |
|---|---|
| **Domain** | Entities, Value Objects, Aggregates, domain-defined port interfaces. Pure business rules — zero external dependencies. |
| **Application** | Use-case services that orchestrate domain objects. Depends only on the Domain layer. |
| **Infrastructure** | Adapters that implement domain ports (persistence, external APIs, messaging). Depends on Domain and Application. |
| **Presentation** | UI / delivery adapters (TUI, REST, CLI). Depends on Application. |

> **In this project** `core/` hosts both the Domain and Application layers:
> - `core/models/` — Domain (Entities, Value Objects)
> - `core/ports/` — Domain (port interfaces owned by the domain)
> - `core/services/` — Application (use-case orchestration)

```
src/task_tracker_tui/
├── core/
│   ├── models/     ← Domain — Entities and Value Objects
│   ├── ports/      ← Domain — port interfaces defined by the domain
│   └── services/   ← Application — use-case services
├── infrastructure/ ← Infrastructure — adapters implementing domain ports
└── presentation/   ← Presentation — UI adapters
```

## Dependency Rule — Inner Layers Cannot Depend on Outer Layers

Dependencies flow **inward only**. Every layer may only import from layers closer to the centre. No exceptions.

```
         ┌───────────────────────────────────┐
         │          presentation             │  ← outermost
         │  ┌─────────────────────────────┐  │
         │  │       infrastructure        │  │
         │  │  ┌───────────────────────┐  │  │
         │  │  │      application      │  │  │
         │  │  │  ┌─────────────────┐  │  │  │
         │  │  │  │     domain      │  │  │  │  ← innermost
         │  │  │  └─────────────────┘  │  │  │
         │  │  └───────────────────────┘  │  │
         │  └─────────────────────────────┘  │
         └───────────────────────────────────┘
```

**Allowed directions:**
- `presentation` → `application` ✅
- `presentation` → `domain` ✅
- `infrastructure` → `domain` ✅
- `application` → `domain` ✅

**Forbidden directions (inner → outer):**
- `domain` → `application` ❌
- `domain` → `infrastructure` ❌
- `domain` → `presentation` ❌
- `application` → `infrastructure` ❌
- `application` → `presentation` ❌
- `infrastructure` → `presentation` ❌

```python
# ✅ Correct — application (core/services) imports only domain (core/models, core/ports)
# src/task_tracker_tui/core/services/create_task_service.py
from task_tracker_tui.core.models.task import Task
from task_tracker_tui.core.ports.task_repository import TaskRepository


# ❌ Wrong — domain imports infrastructure (inner depends on outer)
# src/task_tracker_tui/core/models/task.py
from task_tracker_tui.infrastructure.persistence.json_task_repository import JsonTaskRepository


# ❌ Wrong — application imports infrastructure (inner depends on outer)
# src/task_tracker_tui/core/services/create_task_service.py
from task_tracker_tui.infrastructure.persistence.json_task_repository import JsonTaskRepository


# ❌ Wrong — infrastructure imports presentation (inner depends on outer)
# src/task_tracker_tui/infrastructure/persistence/json_task_repository.py
from task_tracker_tui.presentation.screens.task_screen import TaskScreen
```

## Ports (Protocols)
Define every external capability as a `Protocol` inside `core/ports/`. Infrastructure adapters must implement these protocols — the core never knows the concrete type.

```python
# src/task_tracker_tui/core/ports/task_repository.py
from typing import Protocol
from task_tracker_tui.core.models.task import Task


class TaskRepository(Protocol):
    async def save(self, task: Task) -> None: ...
    async def find_by_id(self, task_id: str) -> Task | None: ...
    async def find_all(self) -> list[Task]: ...
    async def delete(self, task_id: str) -> None: ...
```

## Application Services
Services in `core/services/` orchestrate domain logic. They receive ports via constructor injection and contain **no I/O** of their own.

```python
# src/task_tracker_tui/core/services/create_task_service.py
from task_tracker_tui.core.models.task import Task
from task_tracker_tui.core.ports.task_repository import TaskRepository


class CreateTaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def execute(self, title: str, description: str) -> Task:
        task = Task(title=title, description=description)
        await self._repository.save(task)
        return task
```

## Infrastructure Adapters
Adapters live in `infrastructure/` and implement core ports. They are the **only** place where file I/O, databases, or external APIs are touched.

```python
# src/task_tracker_tui/infrastructure/persistence/json_task_repository.py
from task_tracker_tui.core.models.task import Task
from task_tracker_tui.core.ports.task_repository import TaskRepository


class JsonTaskRepository:
    """Implements TaskRepository using a JSON file as storage."""

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    async def save(self, task: Task) -> None:
        ...
```

## Composition Root
Wire all dependencies in `infrastructure/container.py`. No other module should instantiate concrete adapters.

```python
# src/task_tracker_tui/infrastructure/container.py
from task_tracker_tui.core.services.create_task_service import CreateTaskService
from task_tracker_tui.infrastructure.persistence.json_task_repository import JsonTaskRepository


class Container:
    def __init__(self, tasks_file: str) -> None:
        repository = JsonTaskRepository(tasks_file)
        self.create_task_service = CreateTaskService(repository)
```
