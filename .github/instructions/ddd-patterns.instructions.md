---
applyTo: "src/task_tracker_tui/core/**/*.py"
---

# Domain-Driven Design (DDD) Patterns

Apply DDD building blocks inside `core/`. Keep domain concepts explicit and rich. These patterns are language-agnostic; examples below show the Python implementation.

## Entities
An Entity has a unique identity (`task_id`) that persists across state changes. Entities carry behaviour — they are **not** anemic data bags.

```python
# src/task_tracker_tui/core/models/task.py
from dataclasses import dataclass, field
from datetime import datetime

from task_tracker_tui.core.models.task_timer import TaskTimer


@dataclass
class Task:
    """Aggregate root representing a tracked task."""

    title: str
    description: str
    timer: TaskTimer = field(default_factory=TaskTimer)
    task_id: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    notes: str = ""

    def start_timer(self) -> None:
        self.timer.start()

    def pause_timer(self) -> None:
        self.timer.pause()

    def complete(self) -> None:
        self.timer.pause()
        self.completed_at = datetime.now()

    def is_completed(self) -> bool:
        return self.completed_at is not None
```

## Value Objects
A Value Object is defined entirely by its attributes; it has no identity and must be immutable. In Python, use `@dataclass(frozen=True)` to enforce immutability.

```python
# src/task_tracker_tui/core/models/task_timer.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskTimer:
    """Value Object representing timer state."""

    elapsed_minutes: float = 0.0
    is_running: bool = False
    started_at: datetime | None = None

    def start(self) -> "TaskTimer":
        """Return a new TaskTimer in running state."""
        if self.is_running:
            return self
        return TaskTimer(elapsed_minutes=self.elapsed_minutes, is_running=True, started_at=datetime.now())

    def pause(self) -> "TaskTimer":
        """Return a new TaskTimer with accumulated time."""
        if not self.is_running or self.started_at is None:
            return self
        additional = (datetime.now() - self.started_at).total_seconds() / 60
        return TaskTimer(elapsed_minutes=self.elapsed_minutes + additional, is_running=False)
```

## Aggregate Roots
An Aggregate Root is the only entry point to a cluster of related objects. External code must not modify child entities directly — all mutations go through the root.

- `Task` is the Aggregate Root; `TaskTimer` is an internal Value Object.
- Repositories accept and return `Task` objects, never raw `TaskTimer` instances.

## Repositories (Port Abstractions)
Repositories are domain-defined abstractions that hide persistence details. They work with Aggregate Roots only. In Python, declare them as `Protocol` inside `core/ports/`.

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

## Domain Services
Use a Domain Service when an operation involves multiple entities or doesn't naturally belong to a single entity. Domain Services live in `core/services/` and depend only on core abstractions.

```python
# src/task_tracker_tui/core/services/complete_task_service.py
from task_tracker_tui.core.ports.task_repository import TaskRepository


class CompleteTaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def execute(self, task_id: str) -> None:
        task = await self._repository.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Task '{task_id}' not found")
        task.complete()
        await self._repository.save(task)
```

## Ubiquitous Language
Use domain language consistently in all identifiers, docstrings, and comments. Avoid generic names like `Manager`, `Handler`, or `Helper` in domain classes. Prefer names that reflect the bounded context: `Task`, `TaskTimer`, `CompleteTaskService`, `TaskRepository`.
